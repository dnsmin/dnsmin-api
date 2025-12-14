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
            <PageHeader title={'Server Management'}/>
            <Grid container spacing={2}>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Servers" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Auto-Primaries" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Views" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="Networks" value={0}/>
                </Grid>
                <Grid size={{sm: 12, md: 2}} display="flex" justifyContent="center">
                    <StatisticCard label="TSIG Keys" value={0}/>
                </Grid>
            </Grid>
        </>
    );
};

export default Page;
