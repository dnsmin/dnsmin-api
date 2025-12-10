import {IUser} from '@app/types/user';
import {createSlice} from '@reduxjs/toolkit';

let loginRedirect = localStorage.getItem('loginRedirect');

if (loginRedirect === 'null' || loginRedirect === '') {
    loginRedirect = null;
}

export interface AuthState {
    currentUser: IUser | null;
    redirectPath: string | null;
}

const initialState: AuthState = {
    currentUser: null,
    redirectPath: loginRedirect,
};

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCurrentUser: (
            state: AuthState,
            {payload}: { payload: IUser | null }
        ) => {
            state.currentUser = payload;
        },
        setRedirectPath: (
            state: AuthState,
            {payload}: { payload: string | null }
        ) => {
            localStorage.setItem('loginRedirect', payload || '');
            state.redirectPath = payload;
        },
    },
});

export const {setCurrentUser, setRedirectPath} = authSlice.actions;

export default authSlice.reducer;
