# Folder and file-naming starter

From The Handbook for the Recently Enrolled, edited by Haresh Suppiah. CC BY 4.0.

Folder and file-naming starter

Identifiable or restricted material may need a separate approved controlled system. A folder name does not enforce permissions.

Starter structure

project/
  README.md
  admin/
  protocol/
  data/
    00_incoming/
    01_raw_read_only/
    02_interim/
    03_analysis_ready/
    04_release/
  code/
  outputs/
    figures/
    tables/
    reports/
  metadata/
  logs/

Authoritative copy for each folder: [ ]
Folders prohibited from sync, repository or local device: [ ]
Read-only enforcement for raw material: [ ]
Access owner and review date: [ ]

Naming convention

Pattern: [project]_[item]_[context]_[YYYY-MM-DD]_[status-or-version].[ext]

Allowed separators and case: [ ]
Controlled status/version terms: [draft / reviewed / approved / raw / derived / release]
Leave these out. Participant names, sensitive attributes, credentials, unexplained initials, final2 and latest.

README prompts

- purpose and scope of the project;
- owner, contact and last review date;
- where restricted data actually live;
- folder and data-state meanings;
- setup or processing sequence;
- naming, version and metadata rules;
- prohibited actions;
- backup and recovery route; and
- closure or handover instructions.

Guidance: https://hareshsuppiah.github.io/handbook-for-the-recently-enrolled/templates/folder-file-naming.html
