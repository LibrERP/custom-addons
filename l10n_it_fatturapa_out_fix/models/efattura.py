from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import EFatturaOut
import functools


def patch_inner_function(original_method):
    @functools.wraps(original_method)
    def wrapper(self, *args, **kwargs):
        # Store the original method result
        result = original_method(self, *args, **kwargs)

        # Define your replacement inner function
        def patched_get_id_fiscale_iva(partner, prefer_fiscalcode=False):
            """Function overrides the function from the main module"""
            id_paese = partner.country_id.code
            if partner.vat:
                if (id_paese == "IT" and partner.vat.startswith("IT")) or (
                        id_paese == "SM" and partner.vat.startswith("SM")
                ):
                    id_codice = partner.vat[2:]
                elif not partner.vat[:2].isdigit() and partner.vat[2:].isdigit():
                    id_codice = partner.vat[2:]
                elif not partner.vat[:3].isdigit() and partner.vat[3:].isdigit():
                    # Australia and some Spain VATs
                    id_codice = partner.vat[2:]
                elif not partner.vat[:2].isdigit() and partner.vat[2:11].isdigit():
                    # Netherlands
                    id_codice = partner.vat[2:]
                else:
                    id_codice = partner.vat
            elif partner.fiscalcode or id_paese == "IT":
                id_codice = False
            else:
                id_codice = "99999999999"

            if prefer_fiscalcode and partner.fiscalcode:
                id_codice = partner.fiscalcode

            return {
                "id_paese": id_paese,
                "id_codice": id_codice,
            }

        # Replace the original inner function in the result dict
        if isinstance(result, dict):
            result['get_id_fiscale_iva'] = patched_get_id_fiscale_iva

        return result

    return wrapper


# Apply the decorator to monkey patch the method
EFatturaOut.get_template_values = patch_inner_function(EFatturaOut.get_template_values)
