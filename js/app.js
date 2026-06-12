/* ================================================================
   LLM 深度学习课程 — 共享应用逻辑
   ================================================================ */
(function(){
  'use strict';

  var CHAPTERS = [
    {id:1, file:'ch01.html', title:'环境搭建与分词', desc:'BPE、多语 tokenizer、特殊 token 与模型接口契约', sections:16},
    {id:2, file:'ch02.html', title:'嵌入层与位置编码', desc:'TokenEmbedding、word vectors、上下文化表示、RoPE、长上下文与 prompt 表示', sections:19},
    {id:3, file:'ch03.html', title:'单头自注意力', desc:'Scaled Dot-Product Attention、mask、masked softmax、诊断账本与复杂度边界', sections:19},
    {id:4, file:'ch04.html', title:'多头注意力与 MLA', desc:'MHA、GQA、MLA、KV Cache 预算与 checkpoint 转换', sections:12},
    {id:5, file:'ch05.html', title:'Transformer Block', desc:'RMSNorm、SwiGLU、资源估算、稳定性与 interpretability', sections:15},
    {id:6, file:'ch06.html', title:'组装完整 GPT 模型', desc:'GPT-2 124M、MoE、权重加载、logit parity 与 checkpoint 兼容', sections:12},
    {id:7, file:'ch07.html', title:'训练循环', desc:'数据管线、AdamW、scheduler、checkpoint、异常诊断、分布式、MFU 与训练成本', sections:20},
    {id:8, file:'ch08.html', title:'文本生成', desc:'采样、beam、reasoning/test-time compute、speculative 与结构化解码', sections:15},
    {id:9, file:'ch09.html', title:'微调与对齐', desc:'SFT、LoRA、DPO、GRPO、偏好数据、对齐评估与能力保留', sections:18},
    {id:10, file:'ch10.html', title:'推理优化与前沿', desc:'KV Cache、量化、RAG、tool use、服务压测、模型发布包、多模态与推理引擎', sections:23},
    {id:11, file:'ch11.html', title:'经典神经 NLP 与评测', desc:'RNN、Parsing、Seq2Seq、BERT、评测有效性、安全与 Capstone 报告', sections:14}
  ];

  // ---- State helpers (IndexedDB-backed) ----
  function safeGet(k, fb){ return window.IDB ? IDB.get(k, fb) : (function(){ try{var v=localStorage.getItem(k);return v?JSON.parse(v):fb}catch(e){return fb} })() }
  function safeSet(k, v){ if(window.IDB){ IDB.set(k, v) } else { try{ localStorage.setItem(k, JSON.stringify(v)) } catch(e){} } }

  var completed = new Set(safeGet('llm-done', []));
  var currentCh = parseInt(document.body.getAttribute('data-ch')||'0');

  function homeHref(){
    return currentCh === 0 ? 'index.html' : '../index.html';
  }

  function chapterHref(ch){
    return currentCh === 0 ? 'chapters/' + ch.file : ch.file;
  }

  function chaptersWithHref(){
    return CHAPTERS.map(function(ch){
      return {
        id: ch.id,
        file: chapterHref(ch),
        title: ch.title,
        desc: ch.desc,
        sections: ch.sections
      };
    });
  }

  // ---- Sidebar rendering ----
  function renderSidebar(){
    var nav = document.getElementById('sidebar-nav');
    if(!nav) return;
    var html = '<a href="'+homeHref()+'" class="'+(currentCh===0?'active ':'')+'home-link"'+
      (currentCh===0?' aria-current="page"':'')+'>'+
      '<span class="ch-num">⌂</span> 首页</a>';
    CHAPTERS.forEach(function(ch){
      var cls = (ch.id===currentCh?'active ':'')+(completed.has(ch.id)?'completed ':'');
      html += '<a href="'+chapterHref(ch)+'" class="'+cls.trim()+'"'+
        (ch.id===currentCh?' aria-current="page"':'')+'>'+
        '<span class="ch-num">'+ch.id+'</span> '+ch.title+'</a>';
    });
    nav.innerHTML = html;
  }

  function initHomeLinks(){
    document.querySelectorAll('.sidebar-header h1').forEach(function(title){
      if(title.querySelector('a')) return;
      title.innerHTML = '<a href="'+homeHref()+'">'+title.textContent+'</a>';
    });
  }

  function updateProgress(){
    var bar = document.getElementById('progress-bar');
    var txt = document.getElementById('progress-text');
    if(!bar||!txt) return;
    var pct = Math.round(completed.size/CHAPTERS.length*100);
    bar.style.width = pct+'%';
    txt.textContent = completed.size+' / '+CHAPTERS.length;
  }

  function updateCompleteButton(){
    var btn = document.getElementById('mark-complete');
    if(btn) btn.textContent = completed.has(currentCh) ? '✅ 已完成 (点击取消)' : '✓ 标记完成';
  }

  // ---- Mark chapter complete (toggle) ----
  function markComplete(){
    if(completed.has(currentCh)) completed.delete(currentCh);
    else completed.add(currentCh);
    safeSet('llm-done', [...completed]);
    updateProgress();
    renderSidebar();
    updateCompleteButton();
    var btn = document.getElementById('mark-complete');
    if(btn){
      if(completed.has(currentCh)){
        btn.classList.add('celebrate');
        setTimeout(function(){ btn.classList.remove('celebrate'); }, 500);
      }
    }
  }

  // ---- Theme ----
  function getTheme(){ return safeGet('llm-theme', 'light') }
  function toggleTheme(){
    var html = document.documentElement;
    var isDark = html.getAttribute('data-theme')==='dark';
    var next = isDark?'light':'dark';
    html.setAttribute('data-theme', next);
    safeSet('llm-theme', next);
    var icon = document.getElementById('theme-icon');
    var label = document.getElementById('theme-label');
    if(icon) icon.textContent = next==='dark'?'☀️':'🌙';
    if(label) label.textContent = next==='dark'?'浅色模式':'暗色模式';
  }
  function initTheme(){
    var t = getTheme();
    document.documentElement.setAttribute('data-theme', t);
    if(t==='dark'){
      var icon = document.getElementById('theme-icon');
      var label = document.getElementById('theme-label');
      if(icon) icon.textContent='☀️';
      if(label) label.textContent='浅色模式';
    }
  }

  // ---- Font size ----
  function setFontSize(size){
    document.documentElement.setAttribute('data-font', size);
    safeSet('llm-font', size);
    updateFontBtns(size);
  }
  function updateFontBtns(active){
    document.querySelectorAll('.font-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-size')===active);
    });
  }
  function initFontSize(){
    var saved = safeGet('llm-font', 'medium');
    document.documentElement.setAttribute('data-font', saved);
    updateFontBtns(saved);
  }

  // ---- Exercise check (MC) ----
  function checkMC(btn, groupName){
    var exEl = btn.closest('.exercise');
    if(!exEl) return;
    var fb = exEl.querySelector('.feedback');
    var correctAns = exEl.getAttribute('data-answer');
    var explain = exEl.getAttribute('data-explain')||'';
    var selected = exEl.querySelector('input[name="'+groupName+'"]:checked');
    if(!selected){ fb.className='feedback show wrong'; fb.innerHTML='请先选择一个选项'; return; }
    if(selected.value===correctAns){
      fb.className='feedback show correct';
      fb.innerHTML='✅ 正确！ '+explain;
    } else {
      fb.className='feedback show wrong';
      fb.innerHTML='❌ 不正确。 '+explain;
    }
  }

  function showHint(btn){
    var exEl = btn.closest('.exercise');
    var fb = exEl.querySelector('.feedback');
    fb.className='feedback show hint';
    fb.innerHTML='💡 <strong>提示：</strong>'+exEl.getAttribute('data-explain');
  }

  // ---- Back to top ----
  function initBackToTop(){
    var btn = document.getElementById('back-to-top');
    if(!btn) return;
    window.addEventListener('scroll', function(){
      btn.classList.toggle('visible', window.scrollY > 400);
    });
  }

  // ---- Keyboard nav ----
  function initKeyboardNav(){
    document.addEventListener('keydown', function(e){
      var tag = e.target.tagName;
      if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||e.target.isContentEditable) return;
      if(e.key==='Escape'){ document.getElementById('sidebar').classList.remove('open'); return; }
      if(e.key==='ArrowLeft'){
        e.preventDefault();
        var prev = document.querySelector('.chapter-nav a[rel="prev"]');
        if(prev) location.href = prev.href;
      } else if(e.key==='ArrowRight'){
        e.preventDefault();
        var next = document.querySelector('.chapter-nav a[rel="next"]');
        if(next) location.href = next.href;
      }
    });
  }

  // ---- Sidebar toggle (mobile + tablet tap) ----
  function initSidebarToggle(){
    var toggle = document.querySelector('.menu-toggle');
    var sidebar = document.getElementById('sidebar');
    if(!toggle||!sidebar) return;
    toggle.addEventListener('click', function(e){
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });
    // Tablet: tap sidebar to expand when collapsed
    sidebar.addEventListener('click', function(e){
      if(window.innerWidth <= 959 && window.innerWidth > 639 && !sidebar.classList.contains('open')){
        sidebar.classList.add('expanded');
        setTimeout(function(){ sidebar.classList.remove('expanded'); }, 3000);
      }
    });
  }

  // ---- TOC Generation ----
  function initTOC(){
    var chapter = document.querySelector('.chapter');
    if(!chapter) return;
    var sections = chapter.querySelectorAll('section.card[id]');
    if(sections.length < 3) return;
    var toc = document.createElement('div');
    toc.className = 'toc';
    toc.innerHTML = '<h4>📑 本章目录</h4><ol>' +
      Array.from(sections).map(function(s){
        var h3 = s.querySelector('h3');
        var title = h3 ? h3.textContent : s.id;
        return '<li><a href="#'+s.id+'">'+title+'</a></li>';
      }).join('') + '</ol>';
    var subtitle = chapter.querySelector('.reading-time');
    if(subtitle) subtitle.after(toc);
    // Highlight on scroll (throttled via rAF)
    var tocLinks = toc.querySelectorAll('a');
    var _tocRaf = false;
    window.addEventListener('scroll', function(){
      if(_tocRaf) return;
      _tocRaf = true;
      requestAnimationFrame(function(){
        _tocRaf = false;
        var scrollY = window.scrollY + 120;
        sections.forEach(function(s, i){
          if(s.offsetTop <= scrollY && (!sections[i+1] || sections[i+1].offsetTop > scrollY)){
            tocLinks.forEach(function(a){ a.classList.remove('toc-active') });
            if(tocLinks[i]) tocLinks[i].classList.add('toc-active');
          }
        });
      });
    }, {passive: true});
    // Smooth scroll
    tocLinks.forEach(function(a){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var target = document.querySelector(a.getAttribute('href'));
        if(target) window.scrollTo({top:target.offsetTop-30,behavior:'smooth'});
      });
    });
  }

  // ---- Code Copy (with HTTP fallback) ----
  function fallbackCopy(text, cb, btnRef){
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    try{ document.execCommand('copy'); if(cb) cb(); }
    catch(e){ if(btnRef){ btnRef.innerHTML = '⚠'; setTimeout(function(){ btnRef.innerHTML = '📋'; }, 1500); } }
    document.body.removeChild(ta);
  }

  function initCodeCopy(){
    document.querySelectorAll('.code-block').forEach(function(block){
      var wrap = document.createElement('div');
      wrap.className = 'code-block-wrap';
      block.parentNode.insertBefore(wrap, block);
      wrap.appendChild(block);
      var btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.title = '复制代码';
      btn.innerHTML = '📋';
      btn.addEventListener('click', function(){
        var text = block.textContent;
        if(text.endsWith('\n')) text = text.slice(0,-1);
        var done = function(){
          btn.classList.add('copied');
          btn.innerHTML = '✓';
          setTimeout(function(){ btn.classList.remove('copied'); btn.innerHTML = '📋'; }, 2000);
        };
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(text).then(done).catch(function(){
            fallbackCopy(text, done, btn);
          });
        } else {
          fallbackCopy(text, done, btn);
        }
      });
      wrap.appendChild(btn);
    });
  }

  // ---- Reading Progress Bar (GPU-composited transform + rAF throttle) ----
  var _barRaf = false;
  function initReadingBar(){
    var bar = document.createElement('div');
    bar.className = 'reading-bar';
    bar.id = 'reading-bar';
    bar.style.transformOrigin = 'left';
    bar.style.transform = 'scaleX(0)';
    document.body.appendChild(bar);
    window.addEventListener('scroll', function(){
      if(_barRaf) return;
      _barRaf = true;
      requestAnimationFrame(function(){
        _barRaf = false;
        var scrollH = document.documentElement.scrollHeight - window.innerHeight;
        if(scrollH <= 0) return;
        bar.style.transform = 'scaleX(' + Math.min(1, window.scrollY / scrollH) + ')';
      });
    }, {passive: true});
  }

  // ---- Search ----
  var searchIdx = [];
  function buildSearchIdx(){
    searchIdx = [];
    CHAPTERS.forEach(function(ch){
      searchIdx.push({id:ch.id, file:chapterHref(ch), title:ch.title, desc:ch.desc});
    });
  }
  function handleSearch(val){
    var box = document.getElementById('search-results');
    if(!box) return;
    if(!val || val.length < 2){ box.style.display='none'; box.innerHTML=''; return; }
    var q = val.toLowerCase();
    var matches = searchIdx.filter(function(item){
      return item.title.toLowerCase().indexOf(q)>=0 || item.desc.toLowerCase().indexOf(q)>=0;
    });
    if(matches.length===0){
      box.style.display='block';
      box.innerHTML = '<div style="padding:6px 8px;opacity:.5;font-size:.72rem">未找到匹配章节</div>';
    } else {
      box.style.display='block';
      box.innerHTML = matches.map(function(m){
        return '<a href="'+m.file+'" style="display:block;padding:6px 8px;color:var(--sidebar-text);text-decoration:none;border-radius:4px;font-size:.72rem"'+
          ' onmouseover="this.style.background=\'rgba(255,255,255,.08)\'" onmouseout="this.style.background=\'transparent\'">'+
          '<span style="color:var(--accent);font-weight:600">Ch'+m.id+'</span> '+m.title+'</a>';
      }).join('');
    }
  }

  // ---- Init ----
  function init(){
    initTheme();
    initFontSize();
    initHomeLinks();
    renderSidebar();
    updateProgress();
    updateCompleteButton();
    initBackToTop();
    initKeyboardNav();
    initSidebarToggle();
    initTOC();
    initCodeCopy();
    initReadingBar();
    buildSearchIdx();
    // Bind search
    var searchBox = document.getElementById('search-box') || document.querySelector('.search-box');
    if(searchBox) searchBox.addEventListener('input', function(){ handleSearch(this.value); });
    // KaTeX
    if(window.katex){
      var macros = { '\\parallel': '\\mathrel{/\\!\\!/}' };
      function prepareMathNode(el, expr){
        if(!expr) return;
        if(!el.getAttribute('aria-label')) el.setAttribute('aria-label', expr);
        if(!el.getAttribute('role')) el.setAttribute('role', 'img');
      }
      document.querySelectorAll('.katex-inline').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        prepareMathNode(el, expr);
        try{ katex.render(expr, el, {throwOnError:true, strict:false, macros:macros, trust:true}) }
        catch(e){ console.warn('KaTeX inline:', expr, e.message); el.textContent=expr; el.style.color='#cc4444'; }
      });
      document.querySelectorAll('.katex:not(.katex-inline)').forEach(function(el){
        var expr = el.getAttribute('data-expr');
        if(!expr) return;
        prepareMathNode(el, expr);
        try{ katex.render(expr, el, {displayMode:true, throwOnError:true, strict:false, macros:macros, trust:true}) }
        catch(e){ console.warn('KaTeX display:', expr, e.message); el.textContent=expr; el.style.color='#cc4444'; }
      });
    }
  }

  // ---- Profile Management ----
  var PROFILES_KEY = 'llm-profiles';
  var ACTIVE_PROFILE_KEY = 'llm-active-profile';
  var activeProfileId = safeGet(ACTIVE_PROFILE_KEY, null);

  function getProfiles(){ return safeGet(PROFILES_KEY, []) }
  function saveProfiles(list){ safeSet(PROFILES_KEY, list) }
  function getActiveProfile(){
    if(!activeProfileId) return null;
    var profiles = getProfiles();
    for(var i=0; i<profiles.length; i++){ if(profiles[i].id===activeProfileId) return profiles[i] }
    return null;
  }
  function notesKey(ch){ return 'llm-notes-' + activeProfileId + '-ch' + ch }

  function renderProfileArea(){
    var sb = document.querySelector('.sidebar-footer');
    if(!sb) return;
    var area = document.createElement('div');
    area.className = 'profile-area';
    area.id = 'profile-area';
    sb.parentNode.insertBefore(area, sb);
    updateProfileUI();
  }

  function escapeHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;') }
  function escapeJsString(s){ return String(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/\n/g,'\\n').replace(/\r/g,'\\r') }
  function safeColor(c){ return /^#[0-9a-fA-F]{6}$/.test(String(c)) ? c : '#b35c22' }

  function updateProfileUI(){
    var area = document.getElementById('profile-area');
    if(!area) return;
    var profile = getActiveProfile();
    if(profile){
      var safeName = escapeHtml(profile.name);
      area.innerHTML = '<button class="profile-btn" onclick="LLM.openProfileModal()">'+
        '<span class="profile-avatar" style="background:'+safeColor(profile.color)+'">'+safeName.charAt(0).toUpperCase()+'</span>'+
        '<span class="profile-name">'+safeName+'</span>'+
        '<span style="font-size:.65rem;opacity:.5">▼</span></button>';
    } else {
      area.innerHTML = '<button class="profile-btn" onclick="LLM.openProfileModal()" style="justify-content:center">'+
        '👤 登录 / 创建账户</button>';
    }
  }

  function openProfileModal(){
    var overlay = document.getElementById('profile-modal');
    if(!overlay){
      overlay = document.createElement('div');
      overlay.className = 'modal-overlay';
      overlay.id = 'profile-modal';
      overlay.addEventListener('click', function(e){ if(e.target===overlay) closeProfileModal(); });
      document.body.appendChild(overlay);
    }
    renderProfileModal();
    overlay.classList.add('open');
  }

  function closeProfileModal(){
    var overlay = document.getElementById('profile-modal');
    if(overlay) overlay.classList.remove('open');
  }

  function renderProfileModal(){
    var overlay = document.getElementById('profile-modal');
    if(!overlay) return;
    var profiles = getProfiles();
    var current = getActiveProfile();
    var html = '<div class="modal"><h3>👤 用户账户</h3>';
    if(profiles.length > 0){
      html += '<div class="profile-list">';
      profiles.forEach(function(p){
        var safeName = escapeHtml(p.name);
        var safeId = escapeJsString(p.id);
        html += '<div class="profile-list-item'+(current&&current.id===p.id?' active':'')+'" onclick="LLM.selectProfile(\''+safeId+'\')">'+
          '<span class="profile-avatar" style="background:'+safeColor(p.color)+';width:28px;height:28px;font-size:.7rem">'+safeName.charAt(0).toUpperCase()+'</span>'+
          '<span>'+safeName+'</span>'+
          '<button class="del-btn" onclick="event.stopPropagation();LLM.deleteProfile(\''+safeId+'\')">✕</button></div>';
      });
      html += '</div>';
    }
    html += '<div class="field"><label>新建账户</label>'+
      '<input id="new-profile-name" placeholder="输入用户名..." maxlength="20"></div>'+
      '<div class="actions">'+
      '<button class="btn btn-outline" onclick="LLM.closeProfileModal()">关闭</button>'+
      '<button class="btn btn-primary" onclick="LLM.createProfile()">+ 创建</button></div></div>';
    overlay.innerHTML = html;
  }

  function selectProfile(id){
    activeProfileId = id;
    safeSet(ACTIVE_PROFILE_KEY, id);
    updateProfileUI();
    renderProfileModal();
    updateNotesUI();
  }

  function createProfile(){
    var input = document.getElementById('new-profile-name');
    var name = (input?input.value:'').trim();
    if(!name || name.length < 1) return;
    var colors = ['#b35c22','#4f46e5','#059669','#d97706','#7c3aed','#dc2626','#0891b2','#ca8a04'];
    var profile = { id: 'p'+Date.now(), name:name, color:colors[Math.floor(Math.random()*colors.length)], createdAt:Date.now() };
    var profiles = getProfiles();
    profiles.push(profile);
    saveProfiles(profiles);
    selectProfile(profile.id);
  }

  function deleteProfile(id){
    if(!confirm('确定删除此账户及其所有笔记？此操作不可撤销。')) return;
    var profiles = getProfiles().filter(function(p){ return p.id!==id });
    saveProfiles(profiles);
    // Clean up notes
    for(var i=1; i<=10; i++){ try{ if(window.IDB) IDB.remove('llm-notes-'+id+'-ch'+i); else localStorage.removeItem('llm-notes-'+id+'-ch'+i) }catch(e){} }
    if(activeProfileId===id){ activeProfileId=null; safeSet(ACTIVE_PROFILE_KEY, null) }
    updateProfileUI();
    renderProfileModal();
    updateNotesUI();
  }

  // ---- Notes Management ----
  function getNotes(ch){ return safeGet(notesKey(ch), []) }
  function saveNotes(ch, notes){ safeSet(notesKey(ch), notes) }

  function initNotesPanel(){
    if(currentCh < 1) return;
    var panel = document.createElement('div');
    panel.className = 'notes-panel';
    panel.id = 'notes-panel';
    panel.innerHTML = '<div class="notes-panel-header" onclick="LLM.toggleNotes()">'+
      '<span>📝</span><h4>我的笔记</h4><span class="note-count" id="note-count"></span></div>'+
      '<div class="notes-panel-body" id="notes-list"></div>'+
      '<div class="notes-panel-input">'+
      '<textarea id="note-input" placeholder="写笔记... (支持 Markdown)" onkeydown="if(event.key===\'Enter\'&&event.metaKey)LLM.addNote()"></textarea>'+
      '<button class="btn btn-primary" onclick="LLM.addNote()" style="min-height:36px;padding:6px 12px;font-size:.8rem">保存</button></div>';
    document.body.appendChild(panel);

    var toggleBtn = document.createElement('button');
    toggleBtn.className = 'note-toggle-btn';
    toggleBtn.id = 'note-toggle-btn';
    toggleBtn.title = '笔记';
    toggleBtn.innerHTML = '📝';
    toggleBtn.addEventListener('click', function(){ LLM.toggleNotes(); });
    document.body.appendChild(toggleBtn);

    updateNotesUI();
  }

  function updateNotesUI(){
    var panel = document.getElementById('notes-panel');
    var toggleBtn = document.getElementById('note-toggle-btn');
    var hasNotes = false;
    if(currentCh >= 1 && activeProfileId){
      var notes = getNotes(currentCh);
      hasNotes = notes.length > 0;
      var list = document.getElementById('notes-list');
      var count = document.getElementById('note-count');
      if(list){
        if(notes.length===0){
          list.innerHTML = '<div style="font-size:.8rem;color:var(--text-secondary);padding:20px;text-align:center">暂无笔记，在下方输入框中写第一条笔记吧 ✍️</div>';
        } else {
          list.innerHTML = notes.map(function(n){
            var d = new Date(n.timestamp);
            var time = d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');
            var sectionLabel = n.sectionId ? ' ('+n.sectionId+')' : '';
            return '<div class="note-card">'+
              '<div class="note-meta">'+time+sectionLabel+'</div>'+
              '<div class="note-text">'+escapeHtml(n.text)+'</div>'+
              '<button class="note-del" onclick="LLM.deleteNote(\''+n.id+'\')">✕</button></div>';
          }).join('');
        }
      }
      if(count) count.textContent = notes.length + ' 条';
    }
    if(toggleBtn) toggleBtn.classList.toggle('has-notes', hasNotes);
  }

  function toggleNotes(){
    var panel = document.getElementById('notes-panel');
    if(!panel) return;
    if(!activeProfileId){ openProfileModal(); return; }
    panel.classList.toggle('open');
    if(panel.classList.contains('open')){
      updateNotesUI();
      setTimeout(function(){
        var ta = document.getElementById('note-input');
        if(ta) ta.focus();
      }, 300);
    }
  }

  function addNote(){
    if(!activeProfileId){ openProfileModal(); return; }
    var ta = document.getElementById('note-input');
    var text = (ta?ta.value:'').trim();
    if(!text) return;
    // Detect current visible section
    var sectionId = '';
    var sections = document.querySelectorAll('section.card[id]');
    for(var i=0; i<sections.length; i++){
      var rect = sections[i].getBoundingClientRect();
      if(rect.top < window.innerHeight/2 && rect.bottom > 0){ sectionId = sections[i].id; break }
    }
    var note = { id:'n'+Date.now(), text:text, timestamp:Date.now(), sectionId:sectionId };
    var notes = getNotes(currentCh);
    notes.push(note);
    saveNotes(currentCh, notes);
    if(ta) ta.value = '';
    updateNotesUI();
  }

  function deleteNote(noteId){
    var notes = getNotes(currentCh);
    notes = notes.filter(function(n){ return n.id!==noteId });
    saveNotes(currentCh, notes);
    updateNotesUI();
  }

  // ---- Update init ----
  var _origInit = init;
  init = function(){
    _origInit();
    renderProfileArea();
    if(currentCh >= 1) initNotesPanel();
    updateNotesUI();
  };

  // Public API
  window.LLM = {
    checkMC: checkMC,
    showHint: showHint,
    toggleTheme: toggleTheme,
    markComplete: markComplete,
    setFontSize: setFontSize,
    toggleSolution: function(btn){ btn.classList.toggle('open'); btn.nextElementSibling.classList.toggle('open'); },
    openProfileModal: openProfileModal,
    closeProfileModal: closeProfileModal,
    selectProfile: selectProfile,
    createProfile: createProfile,
    deleteProfile: deleteProfile,
    toggleNotes: toggleNotes,
    addNote: addNote,
    deleteNote: deleteNote,
    getChapters: chaptersWithHref
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
