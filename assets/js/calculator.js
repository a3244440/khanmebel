(function(){
// Прайс (₸). Заменить на реальные цены Khan Mebel.
var P={
  kitchen:{fac:{ldsp:135000,mdf:175000,acryl:225000,enamel:255000},
    facName:{ldsp:"ЛДСП",mdf:"МДФ плёнка",acryl:"акрил",enamel:"эмаль"},
    h:{"720":1,"920":1.12,ceil:1.3},hName:{"720":"верх 720","920":"верх 920",ceil:"до потолка"},
    top:{ldsp:28000,compact:85000,stone:170000},topName:{ldsp:"ЛДСП",compact:"компакт-плита",stone:"искусств. камень"},
    hwPrem:38000,layout:{straight:0,corner:45000,u:90000,island:180000},
    layoutName:{straight:"прямая",corner:"угловая",u:"П-образная",island:"с островом"},
    apron:18000,light:12000,tech:25000},
  wardrobe:{type:{coupe:62000,swing:55000,walkin:48000},typeName:{coupe:"Шкаф-купе",swing:"Распашной шкаф",walkin:"Гардеробная"},
    fac:{ldsp:0,mirror:14000,mdf:38000},facName:{ldsp:"ЛДСП",mirror:"зеркало",mdf:"МДФ эмаль"},
    fill:{base:0,plus:30000,max:60000},light:15000},
  hall:{type:{open:85000,closed:110000},mirror:25000,seat:30000},
  tv:{fac:{ldsp:70000,mdf:95000,enamel:130000},facName:{ldsp:"ЛДСП",mdf:"МДФ плёнка",enamel:"эмаль"},wall:35000,light:12000},
  assembly:0.07
};
var WA="77001116291", tab="kitchen", est=[];
function $(id){return document.getElementById(id)}
function rad(n){var e=document.querySelector('input[name="'+n+'"]:checked');return e?e.value:null}
function num(id){return parseFloat($(id).value)}
function chk(id){return $(id).checked}
function fmt(n){return Math.round(n/1000)*1000>=0?(Math.round(n/1000)*1000).toLocaleString("ru-RU")+" ₸":""}
function m(v,d){return v.toFixed(d).replace(".",",")+" м"}

function calc(){
  var L=[],name="",t=0;
  if(tab==="kitchen"){var k=P.kitchen,len=num("k_len"),f=rad("k_fac"),h=rad("k_h"),tp=rad("k_top"),lay=rad("k_layout");
    var body=len*k.fac[f]*k.h[h];L.push(["Модули, "+k.facName[f]+", "+k.hName[h],body]);
    L.push(["Столешница, "+k.topName[tp],len*k.top[tp]]);
    if(k.layout[lay])L.push(["Форма: "+k.layoutName[lay],k.layout[lay]]);
    if(rad("k_hw")==="prem")L.push(["Фурнитура Blum / Hettich",len*k.hwPrem]);
    if(chk("k_apron"))L.push(["Стеновая панель",len*k.apron]);
    if(chk("k_light"))L.push(["LED-подсветка",len*k.light]);
    if(chk("k_tech"))L.push(["Установка техники",k.tech]);
    name="Кухня "+k.layoutName[lay]+" "+m(len,1)+", "+k.facName[f];}
  else if(tab==="wardrobe"){var w=P.wardrobe,W=num("w_w"),H=num("w_h"),ty=rad("w_type"),fc=rad("w_fac"),fl=rad("w_fill"),a=W*H;
    L.push([w.typeName[ty]+", "+a.toFixed(1).replace(".",",")+" м²",a*w.type[ty]]);
    if(w.fac[fc])L.push(["Фасады: "+w.facName[fc],a*w.fac[fc]]);
    if(w.fill[fl])L.push(["Расширенное наполнение",W*w.fill[fl]]);
    if(chk("w_light"))L.push(["LED-подсветка",W*w.light]);
    name=w.typeName[ty]+" "+m(W,1)+" × "+m(H,2)+", "+w.facName[fc];}
  else if(tab==="hall"){var hl=P.hall,HW=num("h_w"),ht=rad("h_type");
    L.push([(ht==="open"?"Открытая прихожая":"Прихожая со шкафом"),HW*hl.type[ht]]);
    if(chk("h_mirror"))L.push(["Зеркало",hl.mirror]);
    if(chk("h_seat"))L.push(["Сиденье",hl.seat]);
    name="Прихожая "+m(HW,1);}
  else{var tv=P.tv,TW=num("tv_w"),tf=rad("tv_fac");
    L.push(["Тумба, "+tv.facName[tf],TW*tv.fac[tf]]);
    if(chk("tv_wall"))L.push(["Панель и полки",TW*tv.wall]);
    if(chk("tv_light"))L.push(["LED-подсветка",TW*tv.light]);
    name="ТВ-зона "+m(TW,1);}
  var sub=L.reduce(function(s,x){return s+x[1]},0);
  L.push(["Доставка и сборка",sub*P.assembly]);
  t=sub*(1+P.assembly);
  return {name:name,lines:L,total:t};
}
function waLink(cur){
  var items=est.length?est:[cur],s=items.reduce(function(a,x){return a+x.total},0);
  var txt="Здравствуйте! Рассчитал(а) мебель на сайте Khan Mebel:\n"+items.map(function(x,i){return (i+1)+". "+x.name+" — ~"+fmt(x.total)}).join("\n")+
    "\nИтого ориентировочно: "+fmt(s)+"\nХочу записаться на замер.";
  return "https://wa.me/"+WA+"?text="+encodeURIComponent(txt);
}
var shown=0,raf=0;
function tween(to){cancelAnimationFrame(raf);var from=shown,t0=performance.now(),d=matchMedia("(prefers-reduced-motion: reduce)").matches?0:650;
  (function step(now){var k=d?Math.min(1,(now-t0)/d):1;k=1-Math.pow(1-k,3);shown=from+(to-from)*k;$("r-total").textContent=fmt(shown);if(k<1)raf=requestAnimationFrame(step)})(performance.now());
  var el=$("r-total");el.classList.remove("bump");void el.offsetWidth;el.classList.add("bump");}
function hero(){var f=tab==="kitchen"?rad("k_fac"):tab==="wardrobe"?rad("w_fac"):tab==="tv"?rad("tv_fac"):"ldsp";if(window.khanHero)window.khanHero.highlight(f)}
function render(){
  var r=calc();
  tween(r.total);
  $("r-range").textContent="Диапазон: "+fmt(r.total*0.9)+" – "+fmt(r.total*1.12);
  $("r-lines").innerHTML=r.lines.map(function(x){return "<div><span>"+x[0]+"</span><span>"+fmt(x[1])+"</span></div>"}).join("");
  $("est").hidden=!est.length;
  $("est-items").innerHTML=est.map(function(x,i){return '<div class="item"><span>'+x.name+'</span><span style="display:flex;gap:4px;align-items:center;white-space:nowrap">'+fmt(x.total)+'<button type="button" data-del="'+i+'" aria-label="Убрать из сметы">×</button></span></div>'}).join("");
  $("est-sum").textContent=fmt(est.reduce(function(a,x){return a+x.total},0));
  $("send").href=waLink(r);
  ["k_len","w_w","h_w","tv_w"].forEach(function(id){$(id+"_v").textContent=m(num(id),1)});
  $("w_h_v").textContent=m(num("w_h"),2);
  hero();
}
document.querySelectorAll(".tab").forEach(function(b){b.addEventListener("click",function(){
  tab=b.dataset.tab;
  document.querySelectorAll(".tab").forEach(function(x){x.setAttribute("aria-selected",x===b?"true":"false")});
  document.querySelectorAll("[data-pane]").forEach(function(p){p.hidden=p.dataset.pane!==tab});
  $("r-title").textContent=b.textContent.trim();render();})});
document.querySelectorAll("[data-pane]").forEach(function(f){f.addEventListener("input",render);f.addEventListener("change",render);f.addEventListener("submit",function(e){e.preventDefault()})});
$("add").addEventListener("click",function(){var r=calc();est.push({name:r.name,total:r.total});
  try{localStorage.setItem("khan_est",JSON.stringify(est))}catch(e){}
  $("add").textContent="✓ Добавлено в смету";setTimeout(function(){$("add").textContent="+ Добавить в смету"},1800);render();});
$("est-items").addEventListener("click",function(e){var i=e.target.getAttribute("data-del");if(i!==null){est.splice(+i,1);
  try{localStorage.setItem("khan_est",JSON.stringify(est))}catch(_){}render();}});
$("toggle-lines").addEventListener("click",function(){var l=$("r-lines"),o=l.hidden;l.hidden=!o;this.setAttribute("aria-expanded",o?"true":"false");this.textContent=o?"Скрыть расчёт":"Из чего цена"});
try{var s=JSON.parse(localStorage.getItem("khan_est")||"[]");if(Array.isArray(s))est=s}catch(e){}
render();
})();
