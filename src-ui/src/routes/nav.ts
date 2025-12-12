import {NavItem} from '@app/types/nav';

export const navItems: NavItem[] = [
    {key: 'dashboard', label: 'Home', path: '/'},
    {key: 'settings', label: 'Settings', path: '/settings'},
    {
        key: 'system', label: 'System', path: '/system', children: [
            {key: 'stopgap_domains', label: 'Stopgap Domains', path: '/stopgap-domains'},
            {key: 'tenants', label: 'Tenants', path: '/tenants'},
            {key: 'clients', label: 'API Clients', path: '/clients'},
            {key: 'users', label: 'Users', path: '/users'},
            {key: 'users-sessions', label: 'User Sessions', path: '/users/sessions'},
        ]
    },
    {key: 'servers', label: 'Servers', path: '/servers'},
    {key: 'zones', label: 'Zones', path: '/zones'},
    {key: 'audits', label: 'Audits', path: '/audits'},
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
