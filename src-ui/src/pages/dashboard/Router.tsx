import * as React from 'react';
import {Routes, Route, Outlet} from 'react-router-dom';
import PrivateRoute from '@app/routes/PrivateRoute';
import UserLayout from '@layouts/user/Layout';
import PageTitle from '@components/PageTitle';
import DashboardIndexPage from '@pages/dashboard/IndexPage';

interface RouterProps {
    baseUrl: string;
}

const Router: React.FC<RouterProps> = ({baseUrl}) => {
    return (
        <>
            <Routes>
                <Route element={<PrivateRoute/>}>
                    <Route element={<UserLayout/>}>
                        <Route element={
                            <Outlet/>
                        }>
                            <Route path="/"
                                   element={<PageTitle title="Dashboard"><DashboardIndexPage baseUrl={baseUrl}/></PageTitle>}/>
                        </Route>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
