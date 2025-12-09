export interface NavItem {
    key: string;
    label: string;
    path: string;
    children?: NavItem[];
}
