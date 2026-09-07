/* Progressive reading aids. No requests, analytics events, or stored free text. */
(() => {
  'use strict';
  document.addEventListener('DOMContentLoaded', () => {
    const main = document.querySelector('main.content');
    const title = main?.querySelector('h1');
    if (!main || !title) return;
    const root = new URL(document.querySelector('.sidebar-logo')?.closest('a')?.href || './index.html', location.href);
    const page = location.pathname;
    const isChecklist = /\/checklists\//.test(page);
    const isTemplate = /\/templates\//.test(page);
    const cleanTitle = title.textContent.trim();
    const status = document.createElement('p');
    status.className = 'reader-status'; status.setAttribute('role', 'status');
    const announce = text => { status.textContent = text; };
    const button = (label, action) => {
      const el = document.createElement('button'); el.type = 'button'; el.textContent = label;
      el.addEventListener('click', action); return el;
    };
    const copy = async text => {
      try { await navigator.clipboard.writeText(text); announce('Copied.'); }
      catch (_) { announce('Copy is unavailable here. Select the text and use your device’s copy command.'); }
    };
    const tools = document.createElement('nav');
    tools.className = 'reader-tools'; tools.setAttribute('aria-label', 'Page tools');
    tools.append(button('Copy page link', () => copy(location.href)), button('Print this page', () => window.print()));
    const feedback = document.createElement('a');
    feedback.textContent = 'Suggest a change';
    const issue = new URL('https://github.com/hareshsuppiah/handbook-for-the-recently-enrolled/issues/new');
    issue.searchParams.set('template', 'share-feedback.yml');
    // Only the published page location is passed; private local addresses never leave the browser.
    const rootPath = new URL('.', root).pathname;
    const relativePage = page.startsWith(rootPath) ? page.slice(rootPath.length) : '';
    const safeRelative = /^(?:(?:chapters|checklists|templates|stuck|contributions)\/[a-zA-Z0-9_/-]+|index|status|resources|references|support|contributing)\.html$/.test(relativePage) ? relativePage : 'index.html';
    const publicPage = new URL(safeRelative, 'https://hareshsuppiah.github.io/handbook-for-the-recently-enrolled/');
    issue.searchParams.set('location', publicPage.href + ' — ' + cleanTitle);
    feedback.href = issue.href; tools.append(feedback);
    const titleBlock = main.querySelector('#title-block-header') || title;
    titleBlock.after(tools); tools.after(status);

    if (isChecklist) {
      const checks = [...main.querySelectorAll('li input[type="checkbox"]')];
      if (checks.length) {
        const panel = document.createElement('section'); panel.className = 'checklist-tools';
        panel.setAttribute('aria-label', 'Use this checklist');
        const count = document.createElement('p'); count.setAttribute('role','status');
        const note = document.createElement('p'); note.textContent = 'Ticks are reminders, not approval or proof of readiness. Leave unknown items unticked and record what you need to check.';
        const rememberLabel = document.createElement('label');
        const remember = document.createElement('input'); remember.type = 'checkbox';
        rememberLabel.append(remember, document.createTextNode(' Remember ticks on this device'));
        const saving = document.createElement('p'); saving.className = 'reader-storage-note';
        const key = 'handbook-checklist-v1:' + publicPage.pathname;
        const items = checks.map((el, i) => {
          const li = el.closest('li'); const text = li.textContent.trim().replace(/\s+/g,' ');
          el.disabled = false; el.id = 'reader-check-' + i;
          el.setAttribute('aria-label', text); // Works with both Quarto task-list renderings.
          return {el, text, id: text};
        });
        let saved = null;
        try { saved = JSON.parse(localStorage.getItem(key)); } catch (_) { /* Session use still works. */ }
        if (saved && saved.version === 1 && Array.isArray(saved.ticks)) {
          remember.checked = true;
          items.forEach(item => { item.el.checked = saved.ticks.includes(item.id); });
        }
        const update = () => {
          count.textContent = items.filter(item => item.el.checked).length + ' of ' + items.length + ' items ticked';
          saving.textContent = remember.checked ? 'Ticks are saved in this browser only. They do not sync. Avoid saving on a shared device.' : 'Ticks last for this page visit unless you choose to remember them.';
          try {
            if (remember.checked) localStorage.setItem(key, JSON.stringify({version:1,ticks:items.filter(item => item.el.checked).map(item => item.id)}));
            else localStorage.removeItem(key);
          } catch (_) { saving.textContent = 'This browser could not save your ticks. You can still use, copy or print this checklist.'; }
        };
        remember.addEventListener('change',update); items.forEach(item => item.el.addEventListener('change',update));
        const actions = document.createElement('div'); actions.className = 'reader-tools';
        let undo = null;
        const undoButton = button('Undo reset', () => { if (undo) items.forEach((item,i) => { item.el.checked = undo[i]; }); undoButton.hidden = true; actions.querySelectorAll('button')[1]?.focus(); update(); });
        undoButton.hidden = true;
        actions.append(button('Copy checklist', () => {
          const excerpt=main.cloneNode(true);
          excerpt.querySelectorAll('nav,.reader-status,.checklist-tools,.skip-link,.anchorjs-link,.header-section-number,script').forEach(el=>el.remove());
          excerpt.querySelectorAll('li input[type="checkbox"]').forEach((el,i)=>el.replaceWith(document.createTextNode(items[i]?.el.checked ? '[x] ' : '[ ] ')));
          copy(excerpt.textContent.replace(/\n[ \t]+/g,'\n').replace(/\n{3,}/g,'\n\n').trim()+'\n\nFull guidance: '+publicPage.href+'\nTicks are reminders, not approval or proof of readiness.');
        }),button('Reset ticks', () => { undo = items.map(item => item.el.checked); items.forEach(item => { item.el.checked=false; }); undoButton.hidden=false; update(); }),undoButton);
        panel.append(count,note,rememberLabel,saving,actions);
        const section = checks[0].closest('section');
        if (section?.querySelector('h2')) section.querySelector('h2').after(panel); else checks[0].closest('ul').before(panel);
        update();
      }
    }
    if (isTemplate) {
      const download = document.createElement('a'); download.textContent='Download editable template (.md)';
      const slug = page.split('/').pop().replace(/\.html$/,'.md');
      download.href = new URL('resources/downloads/'+slug,root).href; download.download=slug;
      tools.append(download);
      main.querySelectorAll('.template-copy pre code').forEach(code => {
        const action = button('Copy blank template', () => copy(code.textContent));
        const row = document.createElement('div'); row.className = 'reader-tools'; row.append(action); code.closest('pre').before(row);
      });
    }
    const toc = document.querySelector('#TOC');
    if (toc) {
      const phoneContents = document.createElement('nav'); phoneContents.className='phone-page-contents';
      phoneContents.setAttribute('aria-label','On this page');
      const heading=document.createElement('p'); heading.textContent='On this page';
      const links=toc.querySelector('ul')?.cloneNode(true);
      if (links) {
        links.querySelectorAll('[id]').forEach(el=>el.removeAttribute('id'));
        phoneContents.append(heading,links);
        const firstSection=main.querySelector('section.level2');
        if(firstSection) firstSection.before(phoneContents);
      }
    }
    const navToggle=document.querySelector('.quarto-secondary-nav button[data-bs-toggle="collapse"]');
    if(navToggle) { navToggle.setAttribute('aria-label','Book contents'); }
    let printDetails = [];
    window.addEventListener('beforeprint', () => {
      printDetails = [...main.querySelectorAll('details')].map(el => ({el,open:el.open}));
      printDetails.forEach(({el}) => { el.open = true; });
    });
    window.addEventListener('afterprint', () => { printDetails.forEach(({el,open}) => { el.open = open; }); });
    const chooser = document.querySelector('[data-route-chooser]');
    if (chooser) {
      const routes = [...document.querySelectorAll('[data-reading-route]')];
      const select = chooser.querySelector('select');
      chooser.hidden=false;
      select.addEventListener('change', () => routes.forEach(route => { route.hidden=!!select.value && route.dataset.readingRoute!==select.value; }));
    }
    if (/\/resources\.html$/.test(page)) {
      const lists = [...main.querySelectorAll('.resource-catalogue table tbody')];
      if (lists.length) {
        const label=document.createElement('label'); label.className='resource-search'; label.textContent='Find a practical resource';
        const input=document.createElement('input'); input.type='search'; input.placeholder='Try meeting, search, data or authorship'; label.append(input);
        const found=document.createElement('p');found.setAttribute('role','status');
        main.querySelector('.resource-catalogue').before(label); label.after(found);
        const rows=lists.flatMap(body=>[...body.rows]);
        input.addEventListener('input',()=>{ const term=input.value.trim().toLocaleLowerCase(); let n=0; rows.forEach(row=>{ row.hidden=!row.textContent.toLocaleLowerCase().includes(term); if(!row.hidden)n++; }); found.textContent=n ? n+' matching resources' : 'No matches. Try a shorter word or clear the search to browse all resources.'; });
      }
    }
  });
})();
