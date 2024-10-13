#!/usr/bin/env bash

pre_commit_file_content="#!/usr/bin/env bash

changed_files=\$(git diff --cached --name-only | awk 'ORS=\",\"')
changed_files=\${changed_files:0:-1}
echo \"changed_files=\${changed_files}\"
make verify_changes CHANGES=\${changed_files}
"

create_pre_commit_file() {
    echo "${pre_commit_file_content}" > .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    git config --local core.hooksPath .git/hooks/
}

$*
