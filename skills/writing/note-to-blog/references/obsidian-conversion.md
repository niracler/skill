# Obsidian Conversion Rules

All Obsidian-specific Markdown syntax conversions for note-to-blog. Standard Markdown SHALL be preserved unchanged.

## Conversion Table

| # | Obsidian Syntax | Output | Notes |
|---|-----------------|--------|-------|
| 1 | `![[image.png]]` | `![](image.png)` | Keep original filename |
| 2 | `![[image.png\|400]]` | `![](image.png)` | Remove size parameter |
| 3 | `![[image.png\|alt text]]` | `![alt text](image.png)` | Treat text without digits as alt |
| 4 | `[[Page Name]]` | `Page Name` | Plain text, remove brackets |
| 5 | `[[Page Name\|display]]` | `display` | Use display text only |
| 6 | `[[Page Name#heading]]` | `Page Name` | Remove heading anchor |
| 7 | `[[Page Name#heading\|display]]` | `display` | Use display text only |

## Callouts

| Obsidian | Output |
|----------|--------|
| `> [!note] title` | `> **Note:** title` |
| `> [!tip] title` | `> **Tip:** title` |
| `> [!warning] title` | `> **Warning:** title` |
| `> [!info] title` | `> **Info:** title` |
| `> [!abstract] title` | `> **Abstract:** title` |
| `> [!todo] title` | `> **Todo:** title` |
| `> [!type]` (no title) | `> **Type:**` |
| `> [!type]-` (folded) | `> **Type:**` (remove fold marker) |

Pattern: capitalize first letter of type, wrap in `**Type:**`.

The blockquote body lines (`> content`) are preserved unchanged.

## Inline Elements

| Obsidian | Output |
|----------|--------|
| `:span[text]{.spoiler}` | `<span class="spoiler">text</span>` |
| `==highlighted==` | `**highlighted**` (bold as fallback) |
| `%%comment%%` | Remove entirely (Obsidian comments) |

## Inline Tags

Inline `#tag` markers in the body text:

1. Collect all unique `#tag` values
2. Merge with frontmatter `tags` field (deduplicate)
3. Remove `#tag` from body text
4. Add merged tags to output frontmatter

**Detection rule**: `#word` at word boundary, not inside code blocks or URLs. Ignore `#` in headings (`## Heading`).

## Frontmatter Field Mapping

| Obsidian Field | Action |
|----------------|--------|
| `title` | Map to output `title` |
| `aliases` | Use first alias as `title` if no `title` field; remove from output |
| `tags` | Merge with inline tags → output `tags` |
| `date` | Remove (output uses today as `pubDate`) |
| `modified` | Remove |
| `date updated` | Remove |
| `score` | Remove |
| `cssclasses` | Remove |
| Other unknown fields | Remove |

## Examples

### Image embed

Input:

```markdown
![[CleanShot 2023-08-30 at 21.54.28@2x.png|400]]
```

Output:

```markdown
![](CleanShot 2023-08-30 at 21.54.28@2x.png)
```

### Wikilink with display text

Input:

```markdown
参考 [[费曼学习法|费曼学习法]] 的方法
```

Output:

```markdown
参考 费曼学习法 的方法
```

### Callout

Input:

```markdown
> [!warning] 注意安全
> 请不要将私钥上传到公开仓库。
```

Output:

```markdown
> **Warning:** 注意安全
> 请不要将私钥上传到公开仓库。
```

### Mixed content

Input:

```markdown
![[diagram.png]]
![standard](https://example.com/image.png)
```

Output:

```markdown
![](diagram.png)
![standard](https://example.com/image.png)
```

Standard Markdown image is preserved unchanged.

## Fallback

For any Obsidian-specific syntax not covered above:

1. Preserve the original text as-is
2. Add `<!-- TODO: manual conversion needed -->` on the next line
3. Continue processing the rest of the file
