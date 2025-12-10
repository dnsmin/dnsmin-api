import * as React from 'react';
import {Grid} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import {DataGridPro, GridColDef, GridActionsCellItem, useGridApiRef} from '@mui/x-data-grid-pro';
import {usersService} from '@app/services/system/users';
import PageHeader from '@components/PageHeader';
import StatisticCard from '@components/cards/StatisticCard';
import UserFormDialog from '@components/forms/UserFormDialog';
import {useEffect} from "react";

interface ViewProps {
    multiTenant?: boolean;
}

const View = ({multiTenant = true}: ViewProps) => {
    const gridApiRef = useGridApiRef();
    const [totalRecords, setTotalRecords] = React.useState(0);
    const [totalFilteredRecords, setTotalFilteredRecords] = React.useState(0);

    const handleEdit = (id: string) => {
        console.log('Edit row with id:', id);
    };

    const handleDelete = (id: string) => {
        console.log('Delete row with id:', id);
    };

    useEffect(() => {
        return usersService.onUsersStateChanged((totalRecords: number, totalFilteredRecords: number) => {
            setTotalRecords(totalRecords);
            setTotalFilteredRecords(totalFilteredRecords);
        });
    }, [gridApiRef]);

    const columns: readonly GridColDef<any>[] = [
        {field: 'id', headerName: 'User ID', width: 300},
        ...(multiTenant ? [{field: 'tenant_id', headerName: 'Tenant ID', width: 300}] : []),
        {field: 'username', headerName: 'Username', width: 200},
        {field: 'email', headerName: 'Email', width: 200},
        {field: 'status', headerName: 'Status', width: 100},
        {field: 'created_at', headerName: 'Created', width: 175},
        {field: 'updated_at', headerName: 'Updated', width: 175},
        {field: 'authenticated_at', headerName: 'Last Login', width: 175},
        {
            field: 'actions',
            type: 'actions',
            headerName: 'Actions',
            width: 100,
            getActions: (params) => [
                <GridActionsCellItem
                    key="edit"
                    icon={<EditIcon/>}
                    label="Edit"
                    onClick={() => handleEdit(params.row.id)}
                    showInMenu
                />,
                <GridActionsCellItem
                    key="delete"
                    icon={<DeleteIcon/>}
                    label="Delete"
                    onClick={() => handleDelete(params.row.id)}
                    showInMenu
                />,
            ],
        },
    ];

    return (
        <>
            <PageHeader title={'User Management'}/>
            <Grid container justifyContent="space-between">
                <Grid size={{sm: 12, md: 6, lg: 4}} paddingY={2}>
                    <Grid container spacing={2}>
                        <Grid size={{sm: 12, md: 6}}>
                            <StatisticCard label="Total Users" value={totalRecords}/>
                        </Grid>
                        <Grid size={{sm: 12, md: 6}}>
                            <StatisticCard label="Total Results" value={totalFilteredRecords}/>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid size={{sm: 12, md: 3, lg: 2}} paddingY={2} display="flex" justifyContent="flex-end"
                      alignItems="flex-end">
                    <UserFormDialog/>
                </Grid>
                <Grid size={12}>
                    <DataGridPro
                        {...usersService.getGridProps(columns, gridApiRef)}
                        autoHeight
                        initialState={{
                            pinnedColumns: {
                                right: ['actions'],
                            },
                        }}
                    />
                </Grid>
            </Grid>
        </>
    );
};

export default View;
