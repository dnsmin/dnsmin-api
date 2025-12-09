import {createSlice} from '@reduxjs/toolkit';

export interface UiState {

}

const initialState: UiState = {

};

export const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {

    },
});

export const {

} = uiSlice.actions;

export default uiSlice.reducer;
