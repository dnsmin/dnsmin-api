import {NavItem} from '@app/types/nav';

export const navItems: NavItem[] = [
    {key: 'dashboard', label: 'Home', path: '/'},
    {key: 'settings', label: 'Settings', path: '/settings', children: [
            {key: 'settings-ui', label: 'User Interface', path: '/ui'},
            {key: 'settings-registration', label: 'Registration', path: '/registration'},
            {key: 'settings-authentication', label: 'Authentication', path: '/authentication'},
            {key: 'settings-synchronization', label: 'Synchronization', path: '/synchronization'},
        ]
    },
    {
        key: 'system', label: 'System', path: '/system', children: [
            {key: 'stopgap_domains', label: 'Stopgap Domains', path: '/stopgap-domains'},
            {key: 'timezones', label: 'Timezones', path: '/timezones'},
            {key: 'tenants', label: 'Tenants', path: '/tenants'},
            {key: 'clients', label: 'API Clients', path: '/clients'},
            {key: 'users', label: 'Users', path: '/users'},
            {key: 'sessions', label: 'Sessions', path: '/sessions'},
        ]
    },
    {key: 'servers', label: 'Servers', path: '/servers', children: [
            {key: 'servers', label: 'Servers', path: '/servers'},
            {key: 'server-tenants', label: 'Tenants', path: '/tenants'},
        ]
    },
    {key: 'zones', label: 'Zones', path: '/zones', children: [
            {key: 'azones', label: 'Authoritative Zones', path: '/authoritative'},
            {key: 'rzones', label: 'Recursive Zones', path: '/recursive'},
        ]
    },
    {key: 'audits', label: 'Audits', path: '/audits', children: [
            {key: 'audits-clients', label: 'API Clients', path: '/clients'},
            {key: 'audits-users', label: 'Users', path: '/users'},
            {key: 'audits-servers', label: 'Servers', path: '/servers'},
            {key: 'audits-zones', label: 'Zones', path: '/zones'},
            {key: 'audits-synchronization', label: 'Synchronization', path: '/synchronization'},
            {key: 'audits-tasks', label: 'Tasks', path: '/tasks'},
        ]
    },
];

export const getNavItem = (key: string, subItemKey?: string): NavItem | false => {
    for (const navItem of navItems) {
        if (navItem.key.toLowerCase() === key.toLowerCase()) {
            if (typeof subItemKey === 'string' && navItem.children) {
                for (const subNavItem of navItem.children) {
                    if (subNavItem.key.toLowerCase() === subItemKey.toLowerCase()) {
                        return subNavItem;
                    }
                }
                return false;
            }
            return navItem;
        }
    }
    return false;
};
