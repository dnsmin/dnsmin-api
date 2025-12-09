import * as React from 'react';
import {Routes, Route, Outlet} from 'react-router-dom';
import {Container} from '@mui/material';
import PrivateRoute from '@app/routes/PrivateRoute';
import UserLayout from '@layouts/user/Layout';
import PageTitle from '@components/PageTitle';
import DashboardIndexPage from '@pages/dashboard/IndexPage';

const Router = () => {
    return (
        <>
            <Routes>
                <Route element={<PrivateRoute/>}>
                    <Route element={<UserLayout/>}>
                        <Route element={
                            <Container maxWidth={false}>
                                <Outlet/>
                            </Container>
                        }>
                            <Route path="/"
                                   element={<PageTitle title="Dashboard"><DashboardIndexPage/></PageTitle>}/>
                        </Route>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
