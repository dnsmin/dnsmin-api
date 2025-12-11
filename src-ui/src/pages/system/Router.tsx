import * as React from "react";
import {Routes, Route, Outlet} from "react-router-dom";
import PrivateRoute from "@app/routes/PrivateRoute";
import UserLayout from "@layouts/user/Layout";
import PageTitle from "@components/PageTitle";
import SubNavigation from "@components/SubNavigation";
import SystemIndexPage from "@pages/system/IndexPage";
import UsersListView from "@app/features/auth/users/views/ListView";

interface RouterProps {
    basePath: string;
}

const Router: React.FC<RouterProps> = ({basePath}) => {
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
                                   element={
                                <PageTitle title="System Management"><SystemIndexPage basePath={basePath}/></PageTitle>
                            }/>
                            <Route path="/users"
                                   element={
                                <PageTitle title="User Management"><UsersListView basePath={`${basePath}/users`}/></PageTitle>
                            }/>
                            <Route path="/users/:action"
                                   element={
                                <PageTitle title="Create User - User Management"><UsersListView basePath={`${basePath}/users`}/></PageTitle>
                            }/>
                            <Route path="/users/:recordId/:action"
                                   element={
                                <PageTitle title="Update User - User Management"><UsersListView basePath={`${basePath}/users`}/></PageTitle>
                            }/>
                            <Route path="/users/:recordId/:action"
                                   element={
                                <PageTitle title="Delete User - User Management"><UsersListView basePath={`${basePath}/users`}/></PageTitle>
                            }/>
                        </Route>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
