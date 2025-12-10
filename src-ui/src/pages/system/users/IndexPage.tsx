import * as React from 'react';
import {useLocation, useNavigate, useParams} from 'react-router-dom';
import {FormikHelpers} from 'formik';
import {Button, Grid} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import {
    DataGridPro,
    GridColDef,
    GridActionsCellItem,
    GridFilterModel,
    useGridApiRef,
} from '@mui/x-data-grid-pro';
import {IRecordFormMode} from '@app/types/service';
import {IUser} from '@app/types/system/users';
import {usersService} from '@app/services/system/users';
import PageHeader from '@components/PageHeader';
import StatisticCard from '@components/cards/StatisticCard';
import UserFormDialog from '@components/forms/UserFormDialog';
import {toast} from "react-toastify";


interface ViewProps {
    baseUrl: string;
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

const Page = ({baseUrl, multiTenant = true}: ViewProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const {action, userId} = useParams();
    const gridApiRef = useGridApiRef();
    const [filterModel, setFilterModel] = React.useState<GridFilterModel>({
        items: [],
        quickFilterValues: [],
    });
    const [totalRecords, setTotalRecords] = React.useState(0);
    const [totalFilteredRecords, setTotalFilteredRecords] = React.useState(0);
    const [formOpen, setFormOpen] = React.useState(false);
    const [updateRecord, setUpdateRecord] = React.useState<IUser>(defaultRecord);

    const mode: IRecordFormMode = userId ? 'update' : 'create';

    const isFilteringActive = React.useMemo(() => {
        return filterModel.items.length > 0 || (filterModel.quickFilterValues?.length ?? 0) > 0;
    }, [filterModel]);

    const handleFilterModelChange = (newFilterModel: GridFilterModel) => {
        setFilterModel(newFilterModel);
    };

    const openCreate = () => {
        navigate(`${baseUrl}/create`);
    };

    const openUpdate = (id: string) => {
        navigate(`${baseUrl}/${id}/update`);
    };

    const openDelete = (id: string) => {
        navigate(`${baseUrl}/${id}/delete`);
    };

    const closeForm = () => {
        navigate(baseUrl);
    };

    const handleSubmit = async (form: FormikHelpers<IUser>, values: Omit<IUser, 'id'>) => {
        const result = await usersService.saveRecord(values);

        if (typeof result === 'boolean' && result) {
            form.resetForm();
            form.setStatus();
            toast.info('User saved!');
            navigate(baseUrl);
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
        if (!action) {
            setFormOpen(false);
            setUpdateRecord(defaultRecord);
        } else if (action === 'create') {
            setUpdateRecord(defaultRecord);
            setFormOpen(true);
        } else if (action === 'update') {
            const loadRecord = async () => {
                setUpdateRecord(await usersService.getRecord(userId!));
                setFormOpen(true);
            };
            loadRecord();
        } else if (action === 'delete') {
            // TODO: Handle delete view
        } else {
            // TODO: Handle invalid action response
        }
    }, [location.pathname, action, userId]);

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
                        {isFilteringActive && (
                            <Grid size={{sm: 12, md: 6}}>
                                <StatisticCard label="Total Results" value={totalFilteredRecords}/>
                            </Grid>
                        )}
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
                        onFilterModelChange={handleFilterModelChange}
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

export default Page;
