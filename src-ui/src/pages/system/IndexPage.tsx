import * as React from 'react';
import {Grid} from '@mui/material';
import PageHeader from '@components/PageHeader';
import StatisticCard from '@components/cards/StatisticCard';

interface ViewProps {
    basePath: string;
}

const Page: React.FC<ViewProps> = ({basePath}) => {
    return (
        <>
            <PageHeader title={'System Management'}/>
            <Grid container spacing={2}>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Tenants" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Users" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="API Clients" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Stopgap Domains" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="User Sessions" value={0}/>
                </Grid>
            </Grid>
        </>
    );
};

export default Page;
