/* eslint-disable class-methods-use-this */
import ContextProviderJinja from "./ContextProviderJinja";

/**
 * @summary Provides jsonSchema only.
 */
export default class JSONSchemaDataProvider extends ContextProviderJinja {
    get jsonSchema() {
        throw new Error("Not implemented.");
    }
}
