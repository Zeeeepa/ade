import { ContextProviderSchema } from "@mat3ra/esse/dist/js/types";
import ContextProvider from "./ContextProvider";
interface JSONSchemaDataProviderConfig extends ContextProviderSchema {
    isUsingJinjaVariables?: boolean;
}
/**
 * @summary Provides jsonSchema only.
 */
export default class JSONSchemaDataProvider extends ContextProvider {
    isUsingJinjaVariables: boolean;
    constructor(config: JSONSchemaDataProviderConfig);
    get jsonSchema(): void;
}
export {};
