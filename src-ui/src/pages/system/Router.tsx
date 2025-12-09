import * as React from 'react';
import {Routes, Route, Outlet} from 'react-router-dom';
import PrivateRoute from '@app/routes/PrivateRoute';
import UserLayout from '@layouts/user/Layout';
import PageTitle from '@components/PageTitle';
import SubNavigation from '@components/SubNavigation';
import SystemIndexPage from '@pages/system/IndexPage';
import SystemUsersPage from '@pages/system/users/IndexPage';

const Router = () => {
    return (
        <>
            <Routes>
                <Route element={<PrivateRoute/>}>
                    <Route element={<UserLayout/>}>
                        <Route element={
                            <>
                                <SubNavigation baseNavKey={'system'}/>
                                <Outlet/>
                            </>
                        }>
                            <Route path="/"
                                   element={<PageTitle title="System Management"><SystemIndexPage/></PageTitle>}/>
                            <Route path="/users/*"
                                   element={<PageTitle title="User Management"><SystemUsersPage/></PageTitle>}/>
                        </Route>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
