import * as React from 'react';
import {useEffect, useState} from 'react';
import {Routes, Route, useLocation} from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import ReactGA from 'react-ga4';
import {CssBaseline} from '@mui/material';
import {ThemeProvider} from '@mui/material/styles';
import {useAppDispatch} from '@store/store';
import {setCurrentUser} from '@store/reducers/auth';
import {authService} from '@app/services/auth';
import {useTheme} from '@app/components/theme';
import DashboardRouter from '@pages/dashboard/Router';
import UserRouter from '@pages/user/Router';
import SystemRouter from '@pages/system/Router';

import {Loading} from '@components/Loading';

import './App.scss';

const {VITE_NODE_ENV} = import.meta.env;

const App = () => {
    const theme = useTheme();
    const location = useLocation();
    const dispatch = useAppDispatch();
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
                    <Route path="/*" element={<DashboardRouter/>}/>
                    <Route path="/user/*" element={<UserRouter/>}/>
                    <Route path="/system/*" element={<SystemRouter/>}/>
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
