(function(){
  var btn=document.querySelector('.menu-btn'),nav=document.querySelector('.nav');
  if(btn&&nav){btn.addEventListener('click',function(){nav.classList.toggle('open');});}
  var yr=document.getElementById('yr'); if(yr){yr.textContent=new Date().getFullYear();}
  var fb=document.querySelectorAll('.filters button');
  fb.forEach(function(b){b.addEventListener('click',function(){
    fb.forEach(function(x){x.classList.remove('on');}); b.classList.add('on');
    var f=b.getAttribute('data-f');
    document.querySelectorAll('.card').forEach(function(c){
      c.style.display=(f==='all'||c.getAttribute('data-cat')===f)?'':'none';});
  });});
  var r=document.getElementById('reason');
  if(r){
    var sp=document.getElementById('speaking-fields'),fn=document.getElementById('founder-note');
    var q=new URLSearchParams(location.search).get('reason'); if(q){r.value=q;}
    var upd=function(){sp.hidden=r.value!=='speaking'; fn.hidden=r.value!=='founder';};
    r.addEventListener('change',upd); upd();
  }
})();
