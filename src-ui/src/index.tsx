import React from 'react'
import {createRoot} from 'react-dom/client';
import {ErrorBoundary} from 'react-error-boundary'
import {Provider} from 'react-redux';
import {BrowserRouter} from 'react-router-dom';
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import ReactGA from 'react-ga4';
import {authService} from "@app/services/auth";
import store from '@store/store';
import App from '@app/App';
import ErrorPage from '@app/components/ErrorPage.jsx'
import * as serviceWorker from './serviceWorker';
import './utils/i18n';
import './index.scss';

export const {VITE_NODE_ENV, VITE_GA_ID} = import.meta.env;

if (VITE_NODE_ENV === 'production' && VITE_GA_ID) {
    ReactGA.initialize(VITE_GA_ID);
}

(async () => {
    await authService.init();
    const queryClient = new QueryClient();
    createRoot(document.getElementById('root') as HTMLDivElement).render(
        <React.StrictMode>
            <ErrorBoundary FallbackComponent={ErrorPage}>
                <QueryClientProvider client={queryClient}>
                    <Provider store={store}>
                        <BrowserRouter>
                            <App/>
                        </BrowserRouter>
                    </Provider>
                </QueryClientProvider>
            </ErrorBoundary>
        </React.StrictMode>
    );
})();

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
