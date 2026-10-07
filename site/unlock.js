// Dekrypterer de private personer (AES-256-GCM, nøgle = PBKDF2-SHA256 af kodeordet) og fletter dem ind i DATA.
(function(){
  const KEY = 'tree-pw';
  const b64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
  const store = { get(){ try{ return sessionStorage.getItem(KEY) || localStorage.getItem(KEY); }catch(e){ return null; } },
    set(pw, remember){ try{ sessionStorage.setItem(KEY, pw); if(remember) localStorage.setItem(KEY, pw); }catch(e){} },
    clear(){ try{ sessionStorage.removeItem(KEY); localStorage.removeItem(KEY); }catch(e){} } };
  async function decrypt(pw){
    const blob = DATA.private_blob; if(!blob || !crypto.subtle) throw new Error('nocrypto');
    const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey({name:'PBKDF2', salt:b64(blob.salt), iterations:blob.iter, hash:'SHA-256'}, base, {name:'AES-GCM', length:256}, false, ['decrypt']);
    const pt = await crypto.subtle.decrypt({name:'AES-GCM', iv:b64(blob.iv)}, key, b64(blob.ct));
    return JSON.parse(new TextDecoder().decode(pt));
  }
  function merge(recs){
    const byId = Object.fromEntries(DATA.people.map(p=>[p.id,p]));
    recs.forEach(r=>{ const t = byId[r.id]; if(!t) return; const {patch, ...rest} = r; Object.assign(t, rest, {private:false}); });
  }
  const $ = id => document.getElementById(id);
  function ui(unlocked){ const f=$('lock-form'), o=$('lock-open'), on=$('lock-on'); if(!o) return;
    o.hidden = unlocked; on.hidden = !unlocked; if(unlocked) f.hidden = true; }
  async function start(){
    const pw = store.get(); let ok = false;
    if(pw){ try{ merge(await decrypt(pw)); ok = true; }catch(e){ store.clear(); } }
    ui(ok);
    if(window.MAIN) MAIN(); if(window.POSTER) POSTER();
  }
  document.addEventListener('click', e=>{
    if(e.target.id==='lock-open'){ $('lock-form').hidden=false; $('lock-open').hidden=true; $('lock-pw').focus(); }
    if(e.target.id==='lock-close'){ store.clear(); location.reload(); }
  });
  document.addEventListener('submit', async e=>{
    if(e.target.id!=='lock-form') return; e.preventDefault();
    const pw=$('lock-pw').value; $('lock-err').textContent='';
    try{ await decrypt(pw); store.set(pw, $('lock-rem').checked);
      if(store.get()===pw) location.reload();
      else { merge(await decrypt(pw)); ui(true); document.querySelectorAll('#ped,#map,#inset,#lifechart,#occchart,#regionchart').forEach(s=>s.innerHTML=''); if(window.MAIN) MAIN(); if(window.POSTER) POSTER(); }
    }catch(err){ $('lock-err').textContent = err.message==='nocrypto' ? 'Browseren kan ikke dekryptere her.' : 'Forkert kodeord. Prøv igen.'; }
  });
  start();
})();
