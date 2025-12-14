import * as React from "react";
import {Routes, Route, Outlet} from "react-router-dom";
import PrivateRoute from "@app/routes/PrivateRoute";
import UserLayout from "@layouts/user/Layout";
import PageTitle from "@components/PageTitle";
import SubNavigation from "@components/SubNavigation";
import SystemIndexPage from "@pages/system/IndexPage";
import StopgapDomainsListView from "@app/features/system/stopgap-domains/views/ListView";
import TimezonesListView from "@app/features/system/timezones/views/ListView";
import TenantsListView from "@app/features/tenants/tenants/views/ListView";
import ClientsListView from "@app/features/auth/clients/views/ListView";
import UsersListView from "@app/features/auth/users/views/ListView";
import SessionsListView from "@app/features/auth/sessions/views/ListView";

interface RouterProps {
    basePath: string;
}

interface RouterRoute {
    path: string;
    title?: string;
    basePath?: string;
    component: React.ElementType;
}

const routes: RouterRoute[] = [
    {path: '/', component: SystemIndexPage, title: 'System Management'},
    {path: '/stopgap-domains', basePath: '/stopgap-domains', component: StopgapDomainsListView, title: 'Stopgap Domains'},
    {path: '/timezones', basePath: '/timezones', component: TimezonesListView, title: 'Timezones'},
    {path: '/tenants', basePath: '/tenants', component: TenantsListView, title: 'Tenants'},
    {path: '/clients', basePath: '/clients', component: ClientsListView, title: 'API Clients'},
    {
        path: '/clients/:action',
        basePath: '/clients',
        component: ClientsListView,
        title: 'Create API Client - API Clients'
    },
    {
        path: '/clients/:recordId/:action',
        basePath: '/clients',
        component: ClientsListView,
        title: 'Update API Client - API Clients'
    },
    {
        path: '/clients/:recordId/:action',
        basePath: '/clients',
        component: ClientsListView,
        title: 'Delete API Client - API Clients'
    },
    {path: '/users', basePath: '/users', component: UsersListView, title: 'Users'},
    {path: '/users/:action', basePath: '/users', component: UsersListView, title: 'Create User - Users'},
    {
        path: '/users/:recordId/:action',
        basePath: '/users',
        component: UsersListView,
        title: 'Update User - Users'
    },
    {
        path: '/users/:recordId/:action',
        basePath: '/users',
        component: UsersListView,
        title: 'Delete User - Users'
    },
    {path: '/sessions', basePath: '/sessions', component: SessionsListView, title: 'Sessions'},
];

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
                            {routes.map((route, index) => (
                                <Route key={index} path={route.path}
                                       element={route?.title ? (
                                           <PageTitle title={route.title}>
                                               <route.component
                                                   basePath={basePath + (route?.basePath ? route.basePath : '')}/>
                                           </PageTitle>
                                       ) : (
                                           <>
                                               <route.component
                                                   basePath={basePath + (route?.basePath ? route.basePath : '')}/>
                                           </>
                                       )}
                                />
                            ))}
                        </Route>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
