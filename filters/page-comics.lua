-- Insert an editorially selected, rights-cleared visual when a page has one.

local function project_root()
  local source = debug.getinfo(1, "S").source:gsub("^@", "")
  local directory = source:match("^(.*[/\\])") or ""
  local root = directory:gsub("filters[/\\]$", "")
  return root == "" and "." or root:gsub("[/\\]$", "")
end

local comic_data = dofile(project_root() .. "/filters/page-comics-data.lua")

local function normalise_input_path()
  local input = (quarto and quarto.doc and quarto.doc.input_file) or PANDOC_STATE.input_files[1] or ""
  input = input:gsub("\\", "/")
  for page_path, _ in pairs(comic_data) do
    if input == page_path or input:sub(-#page_path) == page_path then
      return page_path
    end
  end
  return input:gsub("^%./", "")
end

local function relative_asset(page_path, asset_path)
  local depth = select(2, page_path:gsub("/", ""))
  return string.rep("../", depth) .. asset_path
end

local function comic_block(entry, page_path)
  local original = "https://xkcd.com/" .. entry.comic_id .. "/"
  local license = "https://creativecommons.org/licenses/by-nc/2.5/"
  local image_alt = entry.alt_text or ("xkcd comic titled “" .. entry.title .. "”.")
  local image = pandoc.Image({pandoc.Str(image_alt)}, relative_asset(page_path, entry.asset_path), entry.title)
  image.attributes["loading"] = "lazy"
  local linked_image = pandoc.Link({image}, original, "Open the original xkcd comic and transcript")

  return pandoc.Div({
    pandoc.Para({linked_image}),
    pandoc.Para({
      pandoc.Str("“" .. entry.title .. "” (xkcd #" .. entry.comic_id .. ") by Randall Munroe. "),
      pandoc.Link({pandoc.Str("Original comic and transcript")}, original),
      pandoc.Str(". Reused under "),
      pandoc.Link({pandoc.Str("CC BY-NC 2.5")}, license),
      pandoc.Str(" and excluded from the handbook’s CC BY 4.0 licence."),
    }),
  }, pandoc.Attr("", {"handbook-visual", "handbook-comic"}))
end

function Pandoc(doc)
  -- GitHub's Quarto runner may report a nested index page only as `index.qmd`.
  -- Page titles are unique, so title lookup prevents those pages inheriting the
  -- home-page mapping while path lookup remains a safe fallback.
  local page_title = pandoc.utils.stringify(doc.meta.title or "")
  local entry = comic_data["title:" .. page_title]
  local page_path = entry and entry.page_path or normalise_input_path()
  entry = entry or comic_data[page_path]
  if not entry then
    return doc
  end

  -- Optional humour follows the chapter's explanation and practical actions.
  table.insert(doc.blocks, comic_block(entry, page_path))
  return doc
end
