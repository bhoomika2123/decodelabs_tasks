const $ = (id) => document.getElementById(id);
let selected = [];
let supported = [];
const pretty = (s) => s.split(' ').map(w => w ? w[0].toUpperCase()+w.slice(1) : w).join(' ');
async function init(){
    try{
        const r=await fetch('/api/skills');
        const d=await r.json();
        if(!r.ok)throw Error(d.message||'Could not load skills');
        supported=d.skills;
        $('skill-options').innerHTML=supported.map(s=>`<option value="${escapeHtml(pretty(s))}"></option>`).join('');
        renderSuggestions();
    }catch(e){
        showStatus('Could not load supported skills. Check the server and raw_skills.csv.',true)
    }
}
function escapeHtml(v){
        return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))
}
function norm(s){
    let t=String(s).trim().toLowerCase().replace(/\s+/g,' ');
    return ({ml:'machine learning',js:'javascript',postgres:'postgresql',cloud:'cloud computing',api:'apis','scikit learn':'scikit-learn',ux:'ux research',ui:'ui design'})[t]||t
}
function renderSuggestions(){
    const host=$('suggestions');host.innerHTML='';
    supported.slice(0,24).forEach(s=>{
        const b=document.createElement('button');
        b.className='chip'+(selected.includes(s)?' active':'');
        b.textContent=pretty(s);b.type='button';
        b.onclick=()=>toggle(s);host.appendChild(b)
    })
}
function renderSelected(){
    const host=$('selected-skills');
    host.innerHTML='';
    if(!selected.length)host.innerHTML='<span class="empty">No skills selected yet.</span>';
    selected.forEach(s=>{
        const b=document.createElement('button');
        b.className='chip';
        b.type='button';
        b.innerHTML=`${escapeHtml(pretty(s))}<span class="x">×</span>`;
        b.title='Remove skill';
        b.onclick=()=>toggle(s);
        host.appendChild(b)
    });
    $('skill-count').textContent=`${selected.length} selected`;renderSuggestions()
}
function toggle(s){
    s=norm(s);
    if(selected.includes(s))selected=selected.filter(x=>x!==s);
    else selected.push(s);
    renderSelected()
}
function showStatus(msg,error=false){
    $('status').textContent=msg;
    $('status').className='status'+(error?' error':'')
}
$('add-skill').onclick=()=>{
    const v=$('skill-input').value.trim();
    if(!v)return showStatus('Type a skill first.',true);
    toggle(v);
    $('skill-input').value='';
    $('skill-input').focus();showStatus('Skill added.')
};
$('skill-input').addEventListener('keydown',e=>{
    if(e.key==='Enter'){
        e.preventDefault();
        $('add-skill').click()
    }
});
    $('reset').onclick=()=>{
        selected=[];
        renderSelected();
        $('results-section').hidden=true;
        showStatus('Your selection has been reset.')
    };
    $('recommend').onclick=async()=>{
        if(selected.length<3)return showStatus('Please select at least three skills.',true);
        const button=$('recommend');
        button.disabled=true;
        button.textContent='Finding matches…';
        showStatus('Comparing your skills with job roles…');
        try{
            const response=await fetch('/api/recommend',{
                method:'POST',headers:{
                    'Content-Type':'application/json'
                },body:JSON.stringify({
                    skills:selected
                })
            });
            const data=await response.json();
            if(!response.ok)
                throw Error(data.message||'Recommendation failed');
            renderResults(data);
            showStatus(data.unrecognized_skills.length?`Unrecognized skills: ${
                data.unrecognized_skills.join(', ')
            }. These were not used for matching.`:'Recommendations generated successfully.');
        }catch(e){
            showStatus(e.message,true)
        }finally{
            button.disabled=false;button.innerHTML='Generate recommendations <span>→</span>'
        }
    };
function renderResults(data){
    $('results-section').hidden=false;
    $('result-note').textContent=data.message;
    const host=$('results');
    host.innerHTML='';
    data.recommendations.forEach((r,i)=>{
        const card=document.createElement('article');
        card.className='result-card';
        const mini=(items,matched=false)=>items.length?items.map(s=>`<span class="mini ${
            matched?'matched':''
        }">${
            escapeHtml(pretty(s))
        }</span>`).join(''):'<span class="empty">None</span>';
        card.innerHTML=`<div class="rank">MATCH #${i+1}</div><h3>${escapeHtml(r.job_role)}</h3><div class="category">${escapeHtml(r.category)}</div><div class="score-row"><span>Skill similarity</span><strong>${r.similarity_percent.toFixed(1)}%</strong></div><div class="track"><div class="fill" style="width:${Math.max(0,Math.min(100,r.similarity_percent))}%"></div></div><p>${escapeHtml(r.description)}</p><div class="skill-label">MATCHED SKILLS</div><div class="mini-chips">${mini(r.matched_skills,true)}</div><div class="skill-label">SKILLS TO LEARN</div><div class="mini-chips">${mini(r.missing_skills)}</div>`;host.appendChild(card)});$('results-section').scrollIntoView({behavior:'smooth',block:'start'

        })
 }
init();renderSelected();
