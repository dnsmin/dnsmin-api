import * as React from 'react';
import {useEffect, useState, useRef} from 'react';
import {Routes, Route, useLocation} from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import ReactGA from 'react-ga4';
import {CssBaseline} from '@mui/material';
import {ThemeProvider} from '@mui/material/styles';
import {useAppDispatch} from '@store/store';
import {setCurrentUser} from '@store/reducers/auth';
import {authService} from '@app/services/auth';
import {useTheme} from '@app/components/theme';
import PublicRoute from './routes/PublicRoute';
import PrivateRoute from './routes/PrivateRoute';

import GuestLayout from '@layouts/guest/Layout';
import UserLayout from '@layouts/user/Layout';
import UserLoginPage from '@pages/user/Login';
import DashboardPage from '@pages/dashboard/IndexPage';
import AuthUsersView from '@pages/auth/Users';

import {Loading} from '@components/Loading';

import './App.scss';

const {VITE_NODE_ENV} = import.meta.env;

interface PageTitleProps {
    title: string;
    children?: React.ReactElement;
}

function useDocumentTitle(title: string, prevailOnUnmount: boolean = false) {
    const defaultTitle = useRef(document.title);

    useEffect(() => {
        document.title = title;
    }, [title]);

    useEffect(
        () => () => {
            if (!prevailOnUnmount) {
                document.title = defaultTitle.current;
            }
        },
        []
    );
}

const Page: React.FC<PageTitleProps> = ({title, children}) => {
    const titlePrefix = "DNSMin | ";
    useDocumentTitle(`${titlePrefix}${title}`);
    return children;
}

const App = () => {
    const theme = useTheme();
    const location = useLocation();
    const dispatch = useAppDispatch();
    const [isAppLoading, setIsAppLoading] = useState(true);

    useEffect(() => {
        setIsAppLoading(true);

        const unsubscribe = authService.onAuthStateChanged((user) => {
            console.log(user);
            if (user) {
                dispatch(setCurrentUser(user));
            } else {
                dispatch(setCurrentUser(null));
            }
            setIsAppLoading(false);
        });

        return unsubscribe;
    }, []);

    useEffect(() => {
        if (location && location.pathname && VITE_NODE_ENV === 'production') {
            ReactGA.send({
                hitType: 'pageview',
                page: location.pathname,
            });
        }
    }, [location]);

    if (isAppLoading) {
        return <Loading/>;
    }

    return (
        <>
            <CssBaseline/>
            <ThemeProvider theme={theme}>
                <Routes>
                    <Route element={<GuestLayout/>}>
                        <Route element={<PublicRoute/>}>
                            <Route path="/user/login" element={<Page title="Sign In"><UserLoginPage/></Page>}/>
                            {/*
                            <Route path="/user/register" element={<Page title="Sign Up"><UserRegisterPage/></Page>}/>
                            <Route path="/user/forgot-password" element={<Page title="Forgot Password"><UserForgetPasswordPage/></Page>}/>
                            <Route path="/user/recover-password" element={<Page title="Reset Password"><UserRecoverPasswordPage/></Page>}/>
                            */}
                        </Route>
                    </Route>
                    <Route element={<UserLayout/>}>
                        <Route path="/" element={<PrivateRoute/>}>
                            <Route path="/auth/users" element={<Page title="User Management"><AuthUsersView/></Page>}/>
                            <Route path="/" element={<Page title="Dashboard"><DashboardPage/></Page>}/>
                        </Route>
                    </Route>
                </Routes>
                <ToastContainer
                    autoClose={2000}
                    draggable={false}
                    position="top-right"
                    hideProgressBar={false}
                    newestOnTop
                    closeOnClick
                    rtl={false}
                    pauseOnHover
                />
            </ThemeProvider>
        </>
    );
};

export default App;
