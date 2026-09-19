#!/usr/bin/env bash
#
# d08 — ONE command to set up and run the whole project in a VM.
#
# On a 42 station nothing needs installing: Vagrant + VirtualBox are already in
# the image. This script just points them at roomy local scratch storage (so the
# small NFS home is never touched), boots an Ubuntu 24.04 VM that shares this
# repo (the required host<->VM shared folder), installs the project, and starts
# the Django server.
#
#   ./setup.sh
#
# First run takes a few minutes (downloads the base box + installs deps). Re-run
# any time: the VM and deps are reused and it just starts the server again.
# Storage defaults to /goinfre, then /sgoinfre, then /tmp (override D08_WORKDIR).
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"
USER_NAME="${USER:-$(id -un)}"

for t in vagrant VBoxManage; do
  command -v "$t" >/dev/null 2>&1 || {
    echo "ERROR: '$t' not found — it should be preinstalled on a 42 station." >&2; exit 1; }
done

# Pick roomy scratch storage for the box cache and the VM disk (first writable
# one wins), so the ~2.7 GB NFS home is left alone.
pick_workdir() {
  [ -n "${D08_WORKDIR:-}" ] && { echo "$D08_WORKDIR"; return; }
  local base
  for base in "/goinfre/$USER_NAME" "/sgoinfre/$USER_NAME" "/tmp/$USER_NAME"; do
    mkdir -p "$base" 2>/dev/null && { echo "$base"; return; }
  done
  echo "/tmp/$USER_NAME"
}
WORKDIR="$(pick_workdir)"; mkdir -p "$WORKDIR"
export VAGRANT_HOME="$WORKDIR/.vagrant.d"; mkdir -p "$VAGRANT_HOME"
mkdir -p "$WORKDIR/VirtualBox_VMs"
VBoxManage setproperty machinefolder "$WORKDIR/VirtualBox_VMs" 2>/dev/null || true
echo "==> scratch storage: $WORKDIR"

echo "==> vagrant up (first run downloads the box + installs deps; a few minutes)…"
vagrant up

cat <<EOF

============================================================
 d08 is ready — starting the Django server.
   browse   :  http://127.0.0.1:8000/account
   accounts :  admin/adminadmin (superuser), alice/alicealice, bob/bobbobbob
   new user :  use the "Create account" form on the page
   stop     :  Ctrl-C (VM stays up; 'vagrant halt' to power it off)
============================================================

EOF

# Run the dev server in the foreground; Ctrl-C stops just the server.
exec vagrant ssh -c '~/run.sh'
