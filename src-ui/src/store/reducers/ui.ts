import {createSlice} from '@reduxjs/toolkit';

export interface NavItem {
    label: string;
    path: string;
}

export interface UiState {
    navItems: NavItem[];
}

const initialState: UiState = {
    navItems: [
        {label: 'Home', path: '/'},
        {label: 'Settings', path: '/settings'},
        {label: 'System', path: '/system'},
        {label: 'Servers', path: '/servers'},
        {label: 'Zones', path: '/zones'},
        {label: 'Audits', path: '/audits'},
    ],
};

export const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {
        clearNavItems: (state) => {
            state.navItems = []
        },
    },
});

export const {
    clearNavItems,
} = uiSlice.actions;

export default uiSlice.reducer;
