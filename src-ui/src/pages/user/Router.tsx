import * as React from 'react';
import {Routes, Route} from 'react-router-dom';
import PublicRoute from '@app/routes/PublicRoute';
import GuestLayout from '@layouts/guest/Layout';
import PageTitle from '@components/PageTitle';
import UserSignInPage from '@pages/user/Login';

const Router = () => {
    return (
        <>
            <Routes>
                <Route element={<PublicRoute/>}>
                    <Route element={<GuestLayout/>}>
                        <Route path="/login" element={<PageTitle title="User Sign In"><UserSignInPage/></PageTitle>}/>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
