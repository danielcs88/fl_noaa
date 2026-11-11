#!/bin/zsh

auto_commit_and_push() {
    local GREEN="\e[32m" YELLOW="\e[33m" RESET="\e[0m"

    # Stage all changes
    git add --all

    # Bail if nothing to commit
    if git diff --cached --quiet; then
        echo "${YELLOW}Nothing to commit.${RESET}"
        return 0
    fi

    # Get the cached diff for context
    local diff_content
    diff_content=$(git diff --cached --stat)

    # Generate commit message via OpenCode
    echo "${GREEN}🤖 Generating commit message...${RESET}"
    local suggested raw rc
    local log_file="Log/opencode_commit.txt"
    mkdir -p Log
    raw=$(echo "$diff_content" | opencode run -m "opencode/big-pickle" \
        "Write a concise git commit message (under 72 chars) following conventional commits format. \
Prefix with a relevant git-emoji: ✨ feat, 🐛 fix, 🔧 chore, 📝 docs, ♻️ refactor, 🎨 style, \
⚡ perf, 🔥 remove, 🚀 deploy, ✅ test, 🏗️ build, 🔒 security. \
Output ONLY the message text — no quotes, no markdown, no preamble." \
        2>"$log_file")
    rc=$?
    # Keep the raw reply after stderr so failures can be diagnosed
    { echo "--- exit: $rc ---"; echo "$raw"; } >> "$log_file"

    # Last non-empty line: strip colors, any leaked reasoning, and surrounding whitespace
    # (no xargs: it chokes on apostrophes and returns nothing)
    if (( rc == 0 )); then
        suggested=$(echo "$raw" \
            | sed -E $'s/\x1b\\[[0-9;]*m//g' \
            | sed 's/.*<\/think>//' \
            | grep -v '^[[:space:]]*$' \
            | tail -1 \
            | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')
    fi

    # Validate we actually got something usable
    if [[ -z "$suggested" || ${#suggested} -gt 100 ]]; then
        echo "${YELLOW}⚠️  Auto-generated message failed (see $log_file). Falling back to manual.${RESET}"
        tail -3 "$log_file"
        echo -n "Commit message: "
        read suggested
        [[ -z "$suggested" ]] && suggested="chore: update files"
    fi

    # Clean stray backticks or quotes
    suggested=$(echo "$suggested" | sed 's/[`"'"'"']//g')

    echo "${GREEN}📝 Commit: ${suggested}${RESET}"
    git commit -n -m "$suggested" && git push
}

auto_commit_and_push
