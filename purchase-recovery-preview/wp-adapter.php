<?php
// Disabled integration preview. Loading this file registers NO hooks or HTTP routes.
namespace Shustrik\RecoveryPreview;

final class Store {
    private $db, $table;
    public function __construct($db, $table) {
        if (!preg_match('/^[a-zA-Z0-9_]+$/D', $table)) throw new \InvalidArgumentException('table');
        $this->db=$db; $this->table=$table;
    }
    private function query($sql) {
        $n=$this->db->query($sql);
        if ($n===false) throw new \RuntimeException('database operation failed');
        return $n;
    }
    public function insert($id,$expiry) {
        $this->query($this->db->prepare("INSERT IGNORE INTO `{$this->table}` (id,state,generation,expiry,lease_until) VALUES (%s,'ready',0,%d,0)",$id,$expiry));
    }
    public function row($id) {
        return $this->db->get_row($this->db->prepare("SELECT * FROM `{$this->table}` WHERE id=%s",$id),ARRAY_A);
    }
    public function claim($id,$now) {
        $this->query($this->db->prepare("UPDATE `{$this->table}` SET state='expired',generation=generation+1 WHERE id=%s AND expiry<=%d AND state NOT IN ('observed','suppressed','expired')",$id,$now));
        $this->query($this->db->prepare("UPDATE `{$this->table}` SET state='await_reconciliation',generation=generation+1 WHERE id=%s AND state='inflight' AND lease_until<=%d",$id,$now));
        $changed=$this->query($this->db->prepare("UPDATE `{$this->table}` SET state='inflight',generation=generation+1,lease_until=%d WHERE id=%s AND state='ready' AND expiry>%d",$now+30,$id,$now));
        return $changed===1 ? $this->row($id) : null;
    }
    public function transition($id,$generation,$from,$to) {
        if (!in_array($to,['ready','await_reconciliation','suppressed','observed','expired'],true)) throw new \InvalidArgumentException('state');
        return $this->query($this->db->prepare("UPDATE `{$this->table}` SET state=%s,generation=generation+1 WHERE id=%s AND generation=%d AND state=%s",$to,$id,$generation,$from))===1;
    }
    public function suppress($id) {
        $this->query($this->db->prepare("UPDATE `{$this->table}` SET state='suppressed',generation=generation+1 WHERE id=%s AND state NOT IN ('observed','expired')",$id));
    }
    public function expire($now) {
        return $this->query($this->db->prepare("UPDATE `{$this->table}` SET state='expired',generation=generation+1 WHERE expiry<=%d AND state NOT IN ('observed','suppressed','expired')",$now));
    }
}

final class Adapter {
    private $store, $release, $formatter, $enabled;
    public function __construct(Store $store,$release,callable $formatter,$enabled=false) {
        $this->store=$store; $this->release=$release; $this->formatter=$formatter; $this->enabled=$enabled;
    }
    private function eligible($order,$key,$loggedIn,$now) {
        return $this->enabled && $this->release>0 && !$loggedIn && $order
            && $order->get_customer_id()===0 && is_string($key) && $key!=='' && $order->key_is_valid($key)
            && $order->is_paid() && $order->get_date_paid() && $order->get_date_created()
            && $order->get_date_created()->getTimestamp()>=$this->release
            && $order->get_date_created()->getTimestamp()<=$now
            && $order->get_date_paid()->getTimestamp()>=$this->release
            && $order->get_date_paid()->getTimestamp()<=$now
            && $order->get_meta('_googlesitekit_ga_purchase_event_tracked')!=='1';
    }
    private function payload($order) {
        $raw=($this->formatter)($order);
        unset($raw['user_data']);
        if (!isset($raw['id'],$raw['totals'],$raw['items']) || !ctype_digit((string)$raw['id'])
            || strlen((string)$raw['id'])>20 || (string)$raw['id']!==(string)$order->get_id() || !$raw['items']) return null;
        $t=$raw['totals'];
        if (($t['currency_code']??'')!=='USD') return null;
        foreach (['total_price','shipping_total','tax_total'] as $field) {
            if (!isset($t[$field]) || !is_numeric($t[$field]) || !is_finite((float)$t[$field]) || (float)$t[$field]<0) return null;
        }
        // Match installed Site Kit's minor-unit converter for the verified USD stream.
        $p=['transaction_id'=>(string)$raw['id'],'currency'=>'USD','value'=>(int)$t['total_price']/100,
            'shipping'=>(int)$t['shipping_total']/100,'tax'=>(int)$t['tax_total']/100,'items'=>[]];
        foreach ($raw['items'] as $i) {
            if (!isset($i['id'],$i['price'],$i['quantity']) || !is_numeric($i['price']) || (float)$i['price']<0
                || !is_finite((float)$i['price']) || !is_numeric($i['quantity']) || (int)$i['quantity']<1
                || (float)$i['quantity']!=(int)$i['quantity']) return null;
            $item=['item_id'=>(string)$i['id'],'price'=>(int)$i['price']/100,'quantity'=>(int)$i['quantity']];
            if (isset($i['name'])) $item['item_name']=(string)$i['name'];
            if (!empty($i['variation'])) $item['item_variant']=(string)$i['variation'];
            foreach (($i['categories']??[]) as $n=>$category) {
                if ($n>=5) break;
                $item[$n===0?'item_category':'item_category'.($n+1)]=(string)$category['name'];
            }
            $p['items'][]=$item;
        }
        return $p;
    }
    public function prepare($order,$key,$loggedIn,$now) {
        if (!$this->eligible($order,$key,$loggedIn,$now)) return false;
        $p=$this->payload($order); if (!$p) return false;
        $this->store->insert($p['transaction_id'],$order->get_date_paid()->getTimestamp()+72*3600);
        return true;
    }
    public function claim($order,$key,$loggedIn,$consent,$online,$tagReady,$now) {
        if (!$this->eligible($order,$key,$loggedIn,$now)) return null;
        $p=$this->payload($order); if (!$p) return null;
        if ($consent==='denied') { $this->store->suppress($p['transaction_id']); return null; }
        if ($consent!=='granted' || !$online || !$tagReady) return null;
        $row=$this->store->claim($p['transaction_id'],$now);
        return $row ? ['id'=>$p['transaction_id'],'generation'=>(int)$row['generation'],'payload'=>$p] : null;
    }
    // Called at the final authorization boundary; payload is regenerated from current order.
    public function authorize($ticket,$order,$key,$loggedIn,$consent,$now) {
        if (!is_array($ticket) || !isset($ticket['id'],$ticket['generation'])) return null;
        if (!$this->eligible($order,$key,$loggedIn,$now)) return null;
        $p=$this->payload($order); if (!$p || $p['transaction_id']!==$ticket['id']) return null;
        if ($consent==='denied') { $this->store->suppress($ticket['id']); return null; }
        if ($consent!=='granted') return null;
        $row=$this->store->row($ticket['id']);
        if (!$row || (int)$row['expiry']<=$now || (int)$row['lease_until']<=$now) return null;
        if (!$this->store->transition($ticket['id'],$ticket['generation'],'inflight','await_reconciliation')) return null;
        return $p;
    }
}

final class Hook {
    // Capability only: caller must derive these context fields from trusted WP APIs.
    // This file deliberately has no call to wrap(), add_action() or register_rest_route().
    public static function wrap($hook,callable $receipt,$enabled=false,array $context=[]) {
        if (!$enabled) return 'disabled';
        if (($context['target']??'')!=='https://shustrik-maps.com'
            || ($context['sitekit']??'')!=='1.184.0' || ($context['woo']??'')!=='11.2.1'
            || ($context['guest_receipt']??false)!==true || ($context['classic_frontend']??false)!==true
            || ($context['consent_bridge_verified']??false)!==true) return 'environment-not-ready';
        if (!$hook instanceof \WP_Hook) return 'missing-hook';
        $matches=[];
        foreach ($hook->callbacks as $priority=>$callbacks) foreach ($callbacks as $id=>$entry) {
            $candidate=$entry['function']; if (!$candidate instanceof \Closure) continue;
            $r=new \ReflectionFunction($candidate);$bound=$r->getClosureThis();
            // Recognize the existing paid guard only by its verified file and original closure.
            if (!$bound) {
                $file=$r->getFileName();$vars=$r->getStaticVariables();
                if (!$file || !is_file($file) || !in_array(hash_file('sha256',$file),[
                    '666940e505df36627c2c556f680f0a0e3e71a7515c68e994b3f8c6a460b2fbe6',
                    '6a9cfc06e1a93060777df0f8baef7aa54c13908486695a4b6ed5cf8d817b978d'],true)
                    || !($vars['original']??null) instanceof \Closure) continue;
                $r=new \ReflectionFunction($vars['original']);$bound=$r->getClosureThis();
            }
            if (!$bound || !is_a($bound,'Google\\Site_Kit\\Core\\Conversion_Tracking\\Conversion_Event_Providers\\WooCommerce')) continue;
            $file=$r->getFileName();
            if ($priority!==10 || $entry['accepted_args']!==1 || !$file || !is_file($file)
                || hash_file('sha256',$file)!=='82da28caecda75acca747963336c170ddf6399999a91f7ecb7588db0b6182c85') return 'provider-drift';
            $owner=new \ReflectionMethod($bound,'get_wgai_event_names');$owner->setAccessible(true);
            if (in_array('purchase',$owner->invoke($bound),true)) return 'external-purchase-owner';
            $matches[]=[$priority,$id];
        }
        if (count($matches)!==1) return 'ambiguous-or-missing-provider';
        [$priority,$id]=$matches[0];
        $hook->callbacks[$priority][$id]['function']=static function($orderId) use($receipt){$receipt($orderId);};
        return 'replaced'; // Exactly one owner; never invoke the original purchase callback too.
    }
}
