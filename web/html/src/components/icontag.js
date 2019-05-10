/* eslint-disable */
'use strict';

const React = require("react");

function IconTag(props) {

  const icons = {
    "action-failed": "fa fa-times-circle-o fa-1-5x text-danger",
    "action-ok": "fa fa-check-circle-o fa-1-5x text-success",
    "action-pending": "fa fa-clock-o fa-1-5x",
    "action-running": "fa fa-exchange fa-1-5x",
    "errata-bugfix": "fa fa-bug fa-1-5x",
    "errata-enhance": "fa fa-1-5x spacewalk-icon-enhancement",
    "errata-security": "fa fa-shield fa-1-5x",
    "errata-reboot": "fa fa-1-5x fa-refresh",
    "errata-restart": "fa fa-1-5x fa-archive",
    "event-type-errata": "fa spacewalk-icon-patches",
    "event-type-package": "fa spacewalk-icon-packages",
    "event-type-preferences": "fa fa-cog",
    "event-type-system": "fa fa-desktop",
    "file-directory": "fa fa-folder-open-o",
    "file-file": "fa fa-file-text-o",
    "file-symlink": "fa spacewalk-icon-listicon-cfg-symlink",
    "header-action": "fa fa-clock-o",
    "header-activation-key": "fa fa-key",
    "header-calendar": "fa fa-calendar",
    "header-chain": "fa fa-chain",
    "header-channel": "fa spacewalk-icon-software-channels",
    "header-channel-configuration": "fa spacewalk-icon-software-channel-management",
    "header-channel-mapping": "fa fa-retweet",
    "header-chat": "fa fa-comment text-primary",
    "header-clock": "fa fa-clock-o",
    "header-config-system": "fa spacewalk-icon-config-system",
    "header-configuration": "fa spacewalk-icon-manage-configuration-files",
    "header-crash": "fa spacewalk-icon-bug-ex",
    "header-errata": "fa spacewalk-icon-patches",
    "header-errata-add": "fa spacewalk-icon-patch-install",
    "header-errata-del": "fa spacewalk-icon-patch-remove",
    "header-errata-set": "fa spacewalk-icon-patch-set",
    "header-errata-set-add": "fa pacewalk-icon-patchset-install",
    "header-event-history": "fa fa-suitcase",
    "header-file": "fa fa-file-text-o",
    "header-folder": "fa fa-folder-open-o",
    "header-globe": "fa fa-globe",
    "header-help": "fa fa-question-circle spacewalk-help-link",
    "header-info": "fa fa-info-circle",
    "header-kickstart": "fa fa-rocket",
    "header-list": "fa fa-list",
    "header-multiorg-big": "fa fa-sitemap fa-3x",
    "header-note": "fa spacewalk-icon-note-pin",
    "header-organisation": "fa fa-group",
    "header-package": "fa spacewalk-icon-packages",
    "header-package-add": "fa spacewalk-icon-package-add",
    "header-package-del": "fa spacewalk-icon-package-delete",
    "header-package-extra": "fa spacewalk-icon-package-extra",
    "header-package-upgrade": "fa spacewalk-icon-package-upgrade",
    "header-power": "fa fa-power-off",
    "header-preferences": "fa fa-cogs",
    "header-proxy": "fa spacewalk-icon-proxy",
    "header-refresh": "fa fa-refresh",
    "header-reloading": "fa fa-refresh fa-spin",
    "header-sandbox": "fa spacewalk-icon-sandbox",
    "header-schedule": "fa spacewalk-icon-schedule",
    "header-search": "fa fa-search",
    "header-signout": "fa fa-sign-out",
    "header-sitemap": "fa fa-sitemap",
    "header-snapshot": "fa fa-camera",
    "header-snapshot-rollback": "fa spacewalk-icon-snapshot-rollback",
    "header-subscriptions-big": "fa fa-list-alt fa-3x",
    "header-symlink": "fa spacewalk-icon-listicon-cfg-symlink",
    "header-system": "fa fa-desktop",
    "header-system-groups": "fa spacewalk-icon-system-groups",
    "header-system-physical": "fa fa-desktop",
    "header-system-virt-guest": "fa spacewalk-icon-virtual-guest",
    "header-system-virt-host": "fa spacewalk-icon-virtual-host",
    "header-taskomatic": "fa fa-tachometer",
    "header-user": "fa fa-user",
    "header-users-big": "fa fa-group fa-3x",
    "item-add": "fa fa-plus",
    "item-clone": "fa fa-files-o",
    "item-del": "fa fa-trash-o",
    "item-disabled": "fa fa-circle-o text-muted",
    "item-download": "fa fa-download",
    "item-download-csv": "fa spacewalk-icon-download-csv",
    "item-edit": "fa fa-edit",
    "item-enabled": "fa fa-check text-success",
    "item-import": "fa fa-level-down",
    "item-search": "fa fa-eye",
    "item-ssm-add": "fa fa-plus-circle",
    "item-ssm-del": "fa fa-minus-circle",
    "item-upload": "fa fa-upload",
    "item-order": "fa fa-sort",
    "item-error": "fa fa-times text-danger",
    "nav-bullet": "fa fa-caret-right",
    "nav-page-first": "fa fa-angle-double-left",
    "nav-page-last": "fa fa-angle-double-right",
    "nav-page-next": "fa fa-angle-right",
    "nav-page-prev": "fa fa-angle-left",
    "nav-right": "fa fa-arrow-right",
    "nav-up": "fa fa-caret-up",
    "repo-sync": "fa fa-refresh",
    "repo-schedule-sync": "fa fa-calendar",
    "scap-nochange": "fa fa-dot-circle-o fa-1-5x text-info",
    "setup-wizard-creds-edit": "fa fa-pencil",
    "setup-wizard-creds-failed": "fa fa-times-circle-o text-danger",
    "setup-wizard-creds-make-primary": "fa fa-star-o text-starred",
    "setup-wizard-creds-primary": "fa fa-star text-starred",
    "setup-wizard-creds-subscriptions": "fa fa-th-list",
    "setup-wizard-creds-verified": "fa fa-check-square text-success",
    "sort-down": "fa fa-arrow-circle-down",
    "sort-up": "fa fa-arrow-circle-up",
    "spinner": "fa fa-spinner fa-spin",
    "system-state": "fa spacewalk-icon-salt-add",
    "system-bare-metal-legend": "fa fa-1-5x spacewalk-icon-bare-metal",
    "system-bare-metal": "fa spacewalk-icon-bare-metal",
    "system-crit": "fa fa-exclamation-circle fa-1-5x text-danger",
    "system-kickstarting": "fa fa-rocket fa-1-5x",
    "system-locked": "fa fa-lock fa-1-5x",
    "system-ok": "fa fa-check-circle fa-1-5x text-success",
    "system-physical": "fa fa-desktop fa-1-5x",
    "system-reboot": "fa fa-refresh",
    "system-unentitled": "fa fa-times-circle fa-1-5x",
    "system-unknown": "fa fa-question-circle fa-1-5x",
    "system-virt-guest": "fa fa-1-5x spacewalk-icon-virtual-guest",
    "system-virt-host": "fa fa-1-5x spacewalk-icon-virtual-host",
    "system-warn": "fa fa-exclamation-triangle fa-1-5x text-warning",
  };

  return (<i className={icons[props.type] + " " + props.className} title={props.title}></i>);
}

module.exports = {
    IconTag: IconTag
}
