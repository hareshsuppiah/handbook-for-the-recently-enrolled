-- Keep wide tables in a keyboard-accessible scrolling region, including without JS.
function Table(tbl)
  if not quarto.doc.is_format('html') then return nil end
  local caption = pandoc.utils.stringify(tbl.caption.long)
  local name = caption ~= '' and ('Table: ' .. caption) or 'Table; scroll horizontally if needed'
  return pandoc.Div({tbl}, pandoc.Attr('', {'reader-table'}, {role='region', ['aria-label']=name, tabindex='0'}))
end
