import * as React from 'react';
import PageHeader from '@components/PageHeader';

interface ViewProps {
    basePath: string;
}

const Page: React.FC<ViewProps> = ({basePath}) => {
    return (
        <>
            <PageHeader title={'Settings Management'}/>
        </>
    );
};

export default Page;
