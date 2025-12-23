#!/bin/bash

# Markdown 格式化脚本
# 用法: ./format_markdown.sh <file.md> 或 ./format_markdown.sh <directory>
# 安装依赖: brew install markdownlint-cli2 prettier

set -e

if [ -z "$1" ]; then
    echo "用法: $0 <file.md|directory>"
    echo "示例:"
    echo "  $0 article.md          # 格式化单个文件"
    echo "  $0 ./posts/            # 格式化目录下所有 .md 文件"
    exit 1
fi

TARGET="$1"

# 检查依赖
if ! command -v prettier &> /dev/null; then
    echo "错误: 未找到 prettier"
    echo "请安装: brew install prettier"
    exit 1
fi

if ! command -v markdownlint-cli2 &> /dev/null; then
    echo "错误: 未找到 markdownlint-cli2"
    echo "请安装: brew install markdownlint-cli2"
    exit 1
fi

echo "1/2 prettier 格式化表格..."
prettier --write "$TARGET"

echo "2/2 markdownlint 检查修复..."
markdownlint-cli2 --fix "$TARGET"

echo "✅ 格式化完成: $TARGET"
