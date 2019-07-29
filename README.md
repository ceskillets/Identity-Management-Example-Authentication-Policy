# Identity Skillet Collections

This repository currently holds two skillet collections for use with the PanHandler framework.

- X509
  - A collection of skillets for managing certificate infrastructure on a PAN-OS firewall
- Authentication Policy
  - A collection of skillets to automate creation of a demo Authentication Policy including all required components. 

## Authentication Policy

This skillet collection will allow you to create a sample authentication policy for use in your environment using either the Okta or Duo MFA providers. PAN-OS Documentation for the feature can be found here: https://docs.paloaltonetworks.com/pan-os/8-1/pan-os-admin/authentication/authentication-policy

You can obtain a free MFA account at the following locations:
- Duo - https://signup.duo.com
- Okta - https://developer.okta.com

It is suggested that before executing the skillets that you create a named configuration snapshot to be able to easily revert the changes that are made. 

### Prerequisites:
- A PAN-OS 8.1 or 9.0 firewall with at least two zones configured
- User-ID enabled in the source zone under test
- Test workstation must be able to communicate with the management interface of the firewall, or you have preconfigured a L3 interface with Response Pages enabled in the interface management profile.
- An Okta or Duo account for use with MFA 

### Executing the Skillets

Depending on the current state of your environment, all skillets may not apply. 

1. Generate an API Key
- If you do not currently have a valid known API key for the firewall use this skillet to generate one
2. Generate a CA on the firewall
- If you already have the authentication portal configured, you may skip this step
- If you do not currently have the authentication portal configured with a valid certificate, and do not wish to generate a CSR for external signing, or import a valid certificate, execute one of 2A or 2B to generate a CA on the firewall to be used to create the required certificates in later steps. 
3. Create a certificate for use by the authentication portal
- If you alread have the authentication portal configured, you make skip this step
- If you have generated a CA in step 2 or have an existing on box CA, use 3A or 3B to generate a certificate using that CA
- If you would like to generate a certificate signing request for an external CA use 3C
  - The CSR will be stored in the ~/.pan_cnc/panhandler/repositories/Identity Skillets/working directory
  - After signing the CSR with the external CA, place the certificate PEM file in the same directory and execute 3D to import the certificate
- If you have a pkcs12 file from an external CA that you would like to import, use 3E
 - Place your pkcs12 file in the ~/.pan_cnc/panhandler/repositories/Identity Skillets/working directory
4. Create a MFA Server profile
 - Execute either 4A or 4B to create the MFA server profile and required components for subsequent use in the Authentication Policy
 - A local auth profile will be created to allow completion of the workflow. Depending on the MFA provider in use, you may need to add additional authentication resources and reconfigure the skeleton objects. 
5. Configure Authentication Portal Settings
 - If you have already configured an Authentication Portal on this firewall, skip this step
 -  This will configure the authentication portal in redirect mode for use by the authentication policy
6. Configure a Sample Authentication Policy
 - This will create an authentication object referencing the authentication profile created in step 4, as well as a sample authentication polciy. 
 - The policy is created in a disabled state. Review your authentication policy rulebase and enable the policy for testing. The policy is limited to testing a single URL in the custom URL category that was created. The default is example.org


 After completing these step, preview the candidate config and commit the changes if appropriate. 

 From a test system in your source zone, access http://example.org 

 You should be redirected to the authentication portal for MFA. 


## X.509

This skillet collection will allow to create and import certificates into PAN-OS.

## Support Policy
The code and templates in the repo are released under an as-is, best effort, support policy. These scripts should be seen as community supported and Palo Alto Networks will contribute our expertise as and when possible. We do not provide technical support or help in using or troubleshooting the components of the project through our normal support options such as Palo Alto Networks support teams, or ASC (Authorized Support Centers) partners and backline support options. The underlying product used (the VM-Series firewall) by the scripts or templates are still supported, but the support is only for the product functionality and not for help in deploying or using the template or script itself. Unless explicitly tagged, all projects or work posted in our GitHub repository (at https://github.com/PaloAltoNetworks) or sites other than our official Downloads page on https://support.paloaltonetworks.com are provided under the best effort policy.


