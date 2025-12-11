import * as React from "react";
import {Routes, Route} from "react-router-dom";
import PublicRoute from "@app/routes/PublicRoute";
import GuestLayout from "@layouts/guest/Layout";
import PageTitle from "@components/PageTitle";
import UserSignInPage from "@pages/user/Login";

interface RouterProps {
    basePath: string;
}

const Router: React.FC<RouterProps> = ({basePath}) => {
    return (
        <>
            <Routes>
                <Route element={<PublicRoute/>}>
                    <Route element={<GuestLayout/>}>
                        <Route path="/login" element={<PageTitle title="User Sign In"><UserSignInPage basePath={`${basePath}/login`}/></PageTitle>}/>
                    </Route>
                </Route>
            </Routes>
        </>
    );
};

export default Router;
