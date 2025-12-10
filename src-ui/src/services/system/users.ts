import {ApiResourceService} from '@app/services/base';
import {IUser, IUserValidationErrors} from '@app/types/system/users';

export class UsersService extends ApiResourceService {
    protected _records: IUser[] = [];

    async getRecord(id: string): Promise<IUser> {
        const response = await this.makeRequest(`${this.apiResourceUrl}/${id}`, undefined, 'GET');
        const data = await response.json();
        return {
            id: data.id,
            tenantId: data.tenant_id || '',
            username: data.username,
            email: data.email,
            phoneNumber: data.phone_number || '',
            status: data.status,
            createdAt: data.created_at,
            updatedAt: data.updated_at,
            authenticatedAt: data.authenticated_at,
        } as IUser;
    }

    async saveRecord(record: IUser): Promise<boolean | IUserValidationErrors> {
        return await super.saveRecord(record);
    }

    get records(): IUser[] {
        return this._records;
    }
}

export const usersService = new UsersService('/api/v1/auth/users');
