import * as React from "react";
import {Routes, Route} from 'react-router-dom';
import {Container} from '@mui/material';
import PageTitle from '@components/PageTitle';
import SubNavigation from '@components/SubNavigation';
import SystemIndexPage from "@pages/system/IndexPage";
import SystemUsersPage from "@pages/system/users/IndexPage";

const Router = () => {
    return (
        <>
            <Container maxWidth={false}>
                <SubNavigation baseNavKey={'system'}/>
                <Routes>
                    <Route path="/" element={<PageTitle title="System Management"><SystemIndexPage/></PageTitle>}/>
                    <Route path="/users" element={<PageTitle title="User Management"><SystemUsersPage/></PageTitle>}/>
                </Routes>
            </Container>
        </>
    );
};

export default Router;
