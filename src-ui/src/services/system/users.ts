import {ApiResourceService} from '@app/services/base';
import {IUser, IUserValidationErrors} from '@app/types/system/users';

export class UsersService extends ApiResourceService {
    protected _records: IUser[] = [];

    async saveRecord(record: IUser): Promise<boolean | IUserValidationErrors> {
        return super.saveRecord(record);
    }

    get records(): IUser[] {
        return this._records;
    }
}

export const usersService = new UsersService('/api/v1/auth/users');
