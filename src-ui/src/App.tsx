import {useEffect, useState} from 'react';
import {Routes, Route, useLocation} from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import ReactGA from 'react-ga4';
import {CssBaseline} from '@mui/material';
import {ThemeProvider} from '@mui/material/styles';

import {authService} from '@app/services/auth';
import {useAppDispatch, useAppSelector} from '@store/store';
import {setCurrentUser} from '@store/reducers/auth';
import {setWindowSize} from '@store/reducers/ui';
import {useWindowSize} from '@app/hooks/useWindowSize';
import {calculateWindowSize} from '@app/utils/helpers';
import {useTheme} from '@app/components/theme';

import PublicRoute from './routes/PublicRoute';
import PrivateRoute from './routes/PrivateRoute';

import UserLayout from '@modules/user/Layout';
import Login from '@modules/login/Login';
import Register from '@modules/register/Register';
import ForgetPassword from '@modules/forgot-password/ForgotPassword';
import RecoverPassword from '@modules/recover-password/RecoverPassword';

import Dashboard from '@pages/Dashboard';
import Dashboard2 from '@pages/Dashboard2';
import Profile from '@pages/profile/Profile';
import AuthUsersView from '@pages/auth/Users';

import {Loading} from './components/Loading';

const {VITE_NODE_ENV} = import.meta.env;

const App = () => {
    const theme = useTheme();
    const location = useLocation();
    const dispatch = useAppDispatch();
    const windowSize = useWindowSize();
    const screenSize = useAppSelector((state) => state.ui.screenSize);
    const [isAppLoading, setIsAppLoading] = useState(true);

    useEffect(() => {
        setIsAppLoading(true);

        const unsubscribe = authService.onAuthStateChanged((user) => {
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
        const size = calculateWindowSize(windowSize.width);
        if (screenSize !== size) {
            dispatch(setWindowSize(size));
        }
    }, [windowSize]);

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
                    <Route path="/user/login" element={<PublicRoute/>}>
                        <Route path="/user/login" element={<Login/>}/>
                    </Route>
                    <Route path="/user/register" element={<PublicRoute/>}>
                        <Route path="/user/register" element={<Register/>}/>
                    </Route>
                    <Route path="/user/forgot-password" element={<PublicRoute/>}>
                        <Route path="/user/forgot-password" element={<ForgetPassword/>}/>
                    </Route>
                    <Route path="/user/recover-password" element={<PublicRoute/>}>
                        <Route path="/user/recover-password" element={<RecoverPassword/>}/>
                    </Route>
                    <Route path="/" element={<PrivateRoute/>}>
                        <Route path="/" element={<UserLayout/>}>
                            <Route path="/auth/users" element={<AuthUsersView/>}/>
                            <Route path="/user/profile" element={<Profile/>}/>
                            <Route path="/" element={<Dashboard/>}/>
                            <Route path="/home2" element={<Dashboard2/>}/>
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
