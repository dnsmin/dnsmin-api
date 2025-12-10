import * as React from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import {FormikHelpers} from 'formik';
import {Button, Grid} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import {DataGridPro, GridColDef, GridActionsCellItem, useGridApiRef} from '@mui/x-data-grid-pro';
import {IRecordFormMode} from '@app/types/service';
import {IUser} from '@app/types/system/users';
import {usersService} from '@app/services/system/users';
import PageHeader from '@components/PageHeader';
import StatisticCard from '@components/cards/StatisticCard';
import UserFormDialog from '@components/forms/UserFormDialog';
import {toast} from "react-toastify";


interface ViewProps {
    multiTenant?: boolean;
}

const defaultRecord: IUser = {
    id: '',
    tenantId: '',
    username: '',
    password: '',
    email: '',
    phoneNumber: '',
    status: '',
    createdAt: '',
    updatedAt: '',
    authenticatedAt: '',
};

const View = ({multiTenant = true}: ViewProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const gridApiRef = useGridApiRef();
    const [totalRecords, setTotalRecords] = React.useState(0);
    const [totalFilteredRecords, setTotalFilteredRecords] = React.useState(0);
    const [formOpen, setFormOpen] = React.useState(false);
    const [updateId, setUpdateId] = React.useState<string | undefined>(undefined);
    const [updateRecord, setUpdateRecord] = React.useState<IUser>(defaultRecord);

    const basePath: string = '/system/users';
    const mode: IRecordFormMode = updateId ? 'update' : 'create';

    const openCreate = () => {
        navigate(`${basePath}/create`);
    };

    const openUpdate = (id: string) => {
        navigate(`${basePath}/${id}/update`);
    };

    const openDelete = (id: string) => {
        navigate(`${basePath}/${id}/delete`);
    };

    const closeForm = () => {
        navigate(basePath);
    };

    const handleSubmit = async (form: FormikHelpers<IUser>, values: Omit<IUser, 'id'>) => {
        const result = await usersService.saveRecord(values);

        if (typeof result === 'boolean' && result) {
            form.resetForm();
            form.setStatus();
            toast.info('User saved!');
            navigate(basePath);
        } else if (typeof result === 'object') {
            form.setErrors(result);
            form.setStatus();
        } else {
            form.setStatus('User could not be saved!');
            toast.error('User could not be saved!');
        }

        form.setSubmitting(false);
    };

    React.useEffect(() => {
        return usersService.onUsersStateChanged((totalRecords: number, totalFilteredRecords: number) => {
            setTotalRecords(totalRecords);
            setTotalFilteredRecords(totalFilteredRecords);
        });
    }, [gridApiRef]);

    React.useEffect(() => {
        if (location.pathname === basePath) {
            setFormOpen(false);
            setUpdateId(undefined);
            setUpdateRecord(defaultRecord);
        } else {
            const uuidRegex = /[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[4][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}/;
            const match = location.pathname.match(uuidRegex);
            if (match) {
                setUpdateId(match[0]);
                // TODO: Load update record with current values
                setUpdateRecord(defaultRecord);
            } else {
                setUpdateId(undefined);
                setUpdateRecord(defaultRecord);
            }
            setFormOpen(true);
        }
    }, [location.pathname]);

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
                    onClick={() => openUpdate(params.row.id)}
                    showInMenu
                />,
                <GridActionsCellItem
                    key="delete"
                    icon={<DeleteIcon/>}
                    label="Delete"
                    onClick={() => openDelete(params.row.id)}
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
                    <Button variant="contained" onClick={() => openCreate()}>Create User</Button>
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
            <UserFormDialog
                open={formOpen}
                mode={mode}
                initialValues={updateRecord}
                onSubmit={handleSubmit}
                onCancel={() => closeForm()}
            />
        </>
    );
};

export default View;
