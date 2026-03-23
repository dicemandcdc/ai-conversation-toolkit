
ACM-46: MongoDB VM Setup — CentOS Stream 10
Overview

Configures the CentOS Stream 10 VM with MongoDB as the primary storage target for Leo AI memories.
Also establishes Git/GitHub integration on the CentOS VM, consistent with the rest of the
ai-conversation-toolkit project.
Jira: ACM-46
Sprint: Sprint 3 (Mar 18-31, 2026)
Depends on: ACM-45 (DOM inspection feasibility confirmed)
Unblocks: ACM-47 (Build export script — MongoDB path)

----------
Environment
| Component       | Value                         |
| --------------- | ----------------------------- |
| OS              | CentOS Stream 10              |
| MongoDB Version | 8.0.20                        |
| Mongosh Version | 2.8.1                         |
| CentOS VM IP    | 192.168.56.101 (Host-Only)    |
| Ubuntu VM IP    | 192.168.56.102 (Host-Only)    |
| Network Adapter | enp0s8 (VirtualBox Host-Only) |
| Git Version     | 2.52.0                        |

----------
Acceptance Criteria
[x] MongoDB service running and enabled on boot
[x] MongoDB version verified and documented
[x] Database created: ai_conversation_toolkit
[x] Collection created: leo_memories
[x] MongoDB user created with least-privilege access
[x] Connection verified from Ubuntu VM (Lenovo desktop)
[x] Git installed and configured on CentOS VM
[x] GitHub SSH key generated and added to GitHub account
[x] Test commit pushed to ai-conversation-toolkit repo from CentOS VM
[x] All credentials stored securely — no hardcoded secrets
[x] Findings documented in docs/ACM-46-mongodb-vm-setup.md
----------
MongoDB Configuration

1. Verify Service Status
sudo systemctl status mongod
sudo systemctl enable mongod
2. Update bindIp in /etc/mongod.conf
net:
port: 27017
bindIp: 127.0.0.1,192.168.56.101
security:
authorization: enabled
3. Open Firewall Port
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload
4. Create Database, Collection, and User
use ai_conversation_toolkit
db.createCollection("leo_memories")
db.createUser({
user: "acm_user",
pwd: "",
roles: [{ role: "readWrite", db: "ai_conversation_toolkit" }]
})
Warning: Password stored securely — not hardcoded in scripts. Use a .env file in ACM-47.
5. Verify Remote Connection from Ubuntu VM
mongosh --host 192.168.56.101 --port 27017 \
-u acm_user -p --authenticationDatabase ai_conversation_toolkit

----------
Network Configuration

Both VMs required a Host-Only network adapter (enp0s8) to communicate.

| VM     | Adapter 1 (NAT) | Adapter 2 (Host-Only) |
| ------ | --------------- | --------------------- |
| CentOS | 10.0.2.15       | 192.168.56.101        |
| Ubuntu | 192.168.1.19    | 192.168.56.102        |

----------
Git Configuration

1. Verify Git Identity
git config --global user.name "dicemandcdc"
git config --global user.email "dicemandcdc@tutamail.com"
git config --global --list
2. Generate SSH Key
ssh-keygen -t ed25519 -C "dicemandcdc@tutamail.com" -f ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
Add public key to GitHub -> Settings -> SSH and GPG Keys -> New SSH Key
Title: CentOS Stream 10 VM
3. Test GitHub Connection
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
Expected: Hi dicemandcdc! You've successfully authenticated...
4. Test Commit
git checkout -b feature/ACM-46-mongodb-setup
echo "ACM-46 MongoDB setup in progress" > ACM-46-test.txt
git add ACM-46-test.txt
git commit -m "ACM-46: Test commit from CentOS VM"
git push -u origin feature/ACM-46-mongodb-setup
PR #16 merged to main. Branch deleted.

----------
Lessons Learned / CentOS Stream Inconsistencies
| Issue                               | Resolution                                                                         |
| ----------------------------------- | ---------------------------------------------------------------------------------- |
| Copy-paste broken (Wayland)         | Typed all commands manually — no workaround found within sprint timebox            |
| VirtualBox Guest Additions failed   | Restored from OVA snapshot (2026-03-19) — Guest Additions deferred                 |
| SSH passphrase confusion            | Removed passphrase for dev VM — acceptable for portfolio project                   |
| Ubuntu VM could not reach CentOS VM | Added Host-Only adapter (enp0s8) to Ubuntu VM                                      |
| mongod.conf authorization misplaced | Placed authorization: enabled under net: instead of security: — corrected manually |

----------
Health Checks

MongoDB health checks deferred — tracked as ACM-23 (backlog).

----------
Credentials

Warning: No credentials are stored in this document or any script.
MongoDB password stored locally only. Will be managed via .env file in ACM-47.

----------
Status

COMPLETE — 2026-03-23
All acceptance criteria met. ACM-47 (Build export script) unblocked.
