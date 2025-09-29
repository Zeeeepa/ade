import type { InMemoryEntity } from "@mat3ra/code/dist/js/entity";
import type { DefaultableInMemoryEntity } from "@mat3ra/code/dist/js/entity/mixins/DefaultableMixin";
import type { NamedInMemoryEntity } from "@mat3ra/code/dist/js/entity/mixins/NamedEntityMixin";
import type { Constructor } from "@mat3ra/code/dist/js/utils/types";
import JSONSchemasInterface from "@mat3ra/esse/dist/js/esse/JSONSchemasInterface";
import type { ApplicationSchemaBase } from "@mat3ra/esse/dist/js/types";
import { ApplicationStandata } from "@mat3ra/standata";

import Executable from "./executable";

type Base = InMemoryEntity & NamedInMemoryEntity & DefaultableInMemoryEntity;

export type BaseConstructor = Constructor<Base> & {
    constructCustomExecutable?: (config: object) => Executable;
};

export type ApplicationConstructor = Constructor<ApplicationMixin> & ApplicationStaticMixin;

export type ApplicationMixin = {
    summary: string | undefined;
    version: string;
    build: string | undefined;
    shortName: string;
    name: string;
    hasAdvancedComputeOptions: boolean;
    isLicensed: boolean;
    isUsingMaterial: boolean;
};

export type ApplicationStaticMixin = {
    defaultConfig: {
        name: string;
        shortName: string;
        version: string;
        summary: string;
        build: string;
    };
    jsonSchema: ApplicationSchemaBase;
};

export function applicationMixin(item: Base) {
    // @ts-expect-error
    const properties: ApplicationMixin & Base = {
        get summary() {
            return this.prop("summary");
        },

        get version() {
            return this.prop("version", "");
        },

        get build() {
            return this.prop("build");
        },

        get shortName() {
            return this.prop("shortName", this.name);
        },

        get hasAdvancedComputeOptions() {
            return this.prop("hasAdvancedComputeOptions", false);
        },

        get isLicensed() {
            return this.prop("isLicensed", false);
        },

        get isUsingMaterial() {
            const materialUsingApplications = ["vasp", "nwchem", "espresso"];
            return materialUsingApplications.includes(this.name);
        },
    };

    Object.defineProperties(item, Object.getOwnPropertyDescriptors(properties));
}

export function applicationStaticMixin<T extends BaseConstructor>(Application: T) {
    const properties: ApplicationStaticMixin = {
        get defaultConfig() {
            const defaultConfigStandata: any =
                new ApplicationStandata().getDefaultConfigByNameAndVersion("espresso", "6.3");
            // TODO: ApplicationStandata should just output this whole object
            return {
                name: defaultConfigStandata.name,
                shortName: defaultConfigStandata.shortName,
                version: defaultConfigStandata.version,
                summary: defaultConfigStandata.summary,
                build: defaultConfigStandata.build,
            };
        },
        get jsonSchema() {
            return JSONSchemasInterface.getSchemaById(
                "software/application",
            ) as ApplicationSchemaBase;
        },
    };

    Object.defineProperties(Application, Object.getOwnPropertyDescriptors(properties));
}
