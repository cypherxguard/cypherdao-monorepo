# Aragon OSx Contracts

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.4.0

### Added

- Use `ProxyLib` and `PluginUpgradeableSetup` from `osx-commons-contracts`.
- Added `VersionComparisonLib` to compare semantic versioning numbers.
- Inherit `ProtocolVersion` in `Plugin`, `PluginCloneable`, `PluginUUPSUpgradeable`, `PluginSetup`, `PermissionCondition`, `PermissionConditionUpgradeable` `PluginSetupProcessor`, `PluginRepoRegistry`, `DAORegistry`, and `ENSSubdomainRegistrar`.
- Added the `FunctionDeprecated` error to `DAO`.
- Added a storage gap to `PluginRepo`.
- Added `initializeFrom` placeholder function to `PluginRepo`.
- `applyMultiTargetPermissions` will revoke when operation is `Grant` and a condition is provided.

### Changed

- Updated `createDao` of the `DAOFactory` to return installed plugins and enable DAO creation without requiring plugins.
- Changed the solidity compiler pragma from `0.8.17` to `^0.8.8` for all files.
- Improved type safety by using `abi.encodeCall` instead of `abi.encodeWithSelector` and the more explicit bracket syntax for permissions.
- Bumped OpenZeppelin dependencies to `4.9.6`.
- Refactored the fallback in the `isGranted` function in `PermissionManager` to make conditions mutually exclusive: Specific conditions answering `false` do not fall back to generic caller conditions (`_who: ANY_ADDR`) or generic target conditions (`_where: ANY_ADDR`).
- Renamed the `signatureValidator` variable in `DAO` to `__removed0`.
- Use the DAOs permission manager functionality to validate signatures.
- Renamed `managingDAO` during deployment to `managementDAO`.
- Aligned contract names during deployment with the names given in `@aragon/osx-commons-configs`.
- Move events `ReleaseMetadataUpdated`and `VersionCreated` from `PluginRepo` to `IPluginRepo`.
- Allow granting permission to `_who: ANY_ADDR`.
- Made ENS registration optional: DAOs and PluginRepos can be registered without a subdomain, but providing subdomain when the protocol doesn't support ENS, will revert with `ENSNotSupported`.

### Removed

- Deleted `AddresslistVoting`, `AddresslistVotingSetup` and related metadata.
- Moved `TokenVoting`, `TokenVotingSetup` and related metadata to the [aragon/token-voting-plugin](https://github.com/aragon/token-voting-plugin) repo.
- Moved `Multisig`, `MultisigSetup` and related metadata to the [aragon/multisig-plugin](https://github.com/aragon/multisig-plugin) repo.
- Moved `Admin`, `AdminSetup` and related metadata to the [aragon/admin-plugin](https://github.com/aragon/admin-plugin) repo.
- Moved

  - interfaces `IDAO`, `IPermissionCondition`, `IPlugin`, `IMembership`, `IProposal`, `IPluginSetup`, `IProtocolVersion`,
  - abstract contracts `DaoAuthorizable`, `DaoAuthorizableUpgradeable`, `Plugin`, `PluginCloneable`, `PluginUUPSUpgradeable`, `PermissionCondition`, `PermissionConditionUpgradeable`, `Addresslist`, `Proposal`, `ProposalUpgradeable`, `PluginSetup`
  - contracts `CloneFactory`
  - libraries `PermissionLib`, `VersionComparisonLib`
  - free functions `auth`, `Proxy`, `BitMap`, `Ratio`, `UncheckedMath`

  to the `osx-commons-contracts` repo.

- Removed unused `MerkleMinter` and `MerkleDistributor` contracts.
- Removed unused `TokenFactory` contract.
- Removed the `SignatureValidatorSet` event from `IDAO`.
- Removed the `setSignatureValidator` function and `signatureValidator` variable in `DAO`. In places, where the function must remain to not alter the `IDAO` interface ID, it will revert and explanatory notes are put in place.
- Removed `active_contracts.json` file and replaced it with `@aragon/osx-commons-configs` package.

### Fixed

- Switch the parameter order in the `MinApprovalsOutOfBounds` error in the `Multisig` plugin.
- Fixed NatSpec comment in `getProposal` function in the `Multisig` plugin.

## v1.3.0

### Added

- Inherit `ProtocolVersion` and `ERC165` in `DAOFactory` and `PluginRepoFactory`.
- Inherit `ProtocolVersion` in `DAO` and `PluginRepo`.
- Added a `nonReentrant` modifier to the `execute` function in the `DAO` contract.
- Added `allowFailureMap` to `IDAO.Executed` event.
- Added `initializeFrom()` reinitializer to `DAO` contract.

### Changed

- Added missing `virtual` keyword to `PermissionCondition` and `PermissionConditionUpgradeable`.
- Added `PermissionCondition` and `PermissionConditionUpgradeable` to have ERC-165 support for `IPermissionCondition` implementations.
- Changed `TokenVotingSetup` to receive the `GovernanceERC20` and `GovernanceWrappedERC20` base contracts as constructor arguments to reduce the `initCode` size because of limitations on the Goerli testnet.
- Revert with errors (`ConditionNotAContract`, `ConditionInterfacNotSupported`) if the `grantWithCondition` function in `PermissionManager` is called with a condition address that is not a `IPermissionCondition` implementation.
- `_grantWithCondition()` doesn't accept `ALLOW_FLAG` anymore as valid condition input.
- Revert with an error (`GrantWithConditionNotSupported`) if the `applySingleTargetPermissions` function in `PermissionManager` is called with `PermissionLib.Operation.GrantWithCondition`.
- Fixed logic bug in the `TokenVoting` and `AddresslistVoting` implementations that caused the `createProposal` function to emit the unvalidated `_startDate` and `_endDate` input arguments (that both can be zero) in the `ProposalCreated` event instead of the validated ones.
- Changed the `createProposal` functions in `Multisig` to allow creating proposals when the `_msgSender()` is listed in the current block.
- Changed the `createProposal` functions in `AddresslistVoting` to allow creating proposals when the `_msgSender()` is listed in the current block.
- Changed the `createProposal` functions in `TokenVoting` to allow creating proposals when the `_msgSender()` owns at least `minProposerVotingPower()` tokens in the current block, also if they are delegated.
- Changed the `isMember` function in the `TokenVoting` plugin to also take delegators of the token into account.
- Fixed and clarified the NatSpec comments according to the Code4rena audit suggestions.
- Changed the solidity compiler pragma from `0.8.17` to `^0.8.8` for files that external developers inherit from.

### Removed

- Removed unnecessary ERC-165 check for `type(UUPSUpgradeable).interfaceId` from `supportsInterface` in `PluginRepo`.

## v1.2.0

### Added

- Adds check to `Multisig.initialize()` that members length isn't bigger than max uint16.
- Added `PlaceholderSetup` contract and adapted deploy scripts.

### Changed

- Added check to `execute()` in `DAO` to prevent griefing attacks if the caller provides insufficient gas on actions being allowed to fail.
- Disallow creating a new proposal in the Multisig plugin in the same block where the settings have been changed.
- Updates `MultisigSetup` to be used as Release 1 Build 2.

## v1.0.1

### Added

- Created the `IMultisig` interface.

### Changed

- Renamed the function `getImplementationAddress` to `implementation` in `IPluginSetup`.
- Moved `NO_CONDITION` constant to `PermissionLib`.
- Use the `calldata` instead of `memory` keyword in `PluginSetup.prepareInstallation`.
- Moved `_disableInitializers` inside the constructors of `PluginCloneable` and `PluginUUPSUpgradeable`.
- Changed license from `MIT` to `AGPL-3.0-or-later`.
- Renamed `DAOSettings.name` to `DAOSettings.subdomain`.
- Fixed the ERC165 interface ID and `supportsInterface` computations.
- Replaced non-upgradeable contract dependencies by upgradeable ones for the cloneable `Admin` plugin.
- Refactored `ProposalBase` into `IProposal`.
- Refactored the `auth` modifier to always use `where = address(this)` and adapted errors.
- Use OZ's upgradeable contracts for `PluginCloneable`.
- Renamed `getDAO()` to `dao()` and changed the `dao` state variable mutability to private.

### Removed

- Removed unused `DaoAuthorizable` dependency from `PluginSetupProcessor`.
- Merged `IMembershipContract` into `IMembership`.
- Removed the `_auth` in `PermissionManager` that allowed for having the `ROOT_PERMISSION_ID` permission for a specific `where` target contract.
- Removed the `WITHDRAW_PERMISSION_ID`.
- Removed `DaoAuthorizableCloneable` and `DaoAuthorizableBase`.
- Moved the array length check for the `MintSettings` from `TokenVotingSetup` into `GovernanceERC20` contract.

## v0.7.0-alpha

### Added

- Added support for release metadata.
- Added `IMembership` and `IMembershipContract` and the `MembershipContractAnnounced` event.
- Added a `metadata.json` file for all plugins.
- Added `startDate` and `endDate` to the `ProposalCreated` event.
- Added the `ProposalBase`, `Proposal`, and `ProposalUpgradeable` contracts to refactor and unify the proposal creation and execution process across all governance plugins.
- Adds `startDate` and `endDate` to Multisig proposals. Execution and approvals of proposals have now to be in the boundaries of these 2 dates.
- Adds `IEIP4824`
- Adds `event NewURI` implementations for `daoURI()` and `setDaoURI()` definitions in `DAO`
- Added check that plugin and DAO subdomains only contain `a-z`, `0-9` or a dash (`-`).
- Adds `allowFailureMap` to the plugins for creating proposals.
- Added verify steps into deployment scripts.

### Changed

- Changed the folder structure of the `contracts` folder.
- Renamed `PreparedDependency` to `PreparedSetupData`.
- Changed `CallbackReceived` which now emits the sender as well.
- Renamed the `AddressesAdded` and `AddressesRemoved` event to `MembersAdded` and `MembersRemoved`.
- Avoided integer division in the `MajorityVoting` execution criteria to avoid precision loss.
- Replaced `ProposalParameters.minParticipation` by `minVotingPower` in `TokenVoting` and `AddresslistVoting`.
- Rescaled and renamed `PCT_BASE = 10**18` to `RATIO_BASE = 10**6`.
- Changed the type of `ProposalParameter.minApprovals`, `MultisigSettingsUpdated.minApprovals` from `uint256` to `uint16`, and added `approvals`(uint16) in the `Proposal` struct.
- Changed `_canVote` logic to revert for votes being cast with `VoteOption.None`.
- Changed `callId` in `DAO.execute()` from `uint256` to `bytes32`.
- Changed the `createProposal` function signature which expects `uint256` `allowFaiureMap` argument.
- Changed all occurences of `oracle` to `condition`.
- Renamed `ItemSingleTarget` and `ItemMultiTarget` in `PermissionLib` to `SingleTargetPermission` and `MultiTargetPermission`.
- Renamed `bulkOnSingleTarget()` and `bulkOnMultiTarget()` in `PermissionManager` to `applySingleTargetPermissions()` and `applyMultiTargetPermissions()`
- Renames plugins `TokenVoting`, `AddresslistVoting`, `Admin` and `multisig` to be compliant to the new naming rules.
- Renames `name` in `PluginRepoRegistry` and `DAORegistry` to `subdomain`.

### Removed

- Removed redundant storage of `totalVotingPower` in `ProposalParameters.Tally` in `TokenVoting` and `AddresslistVoting` and obtain it from `snapshotBlock` and `votingToken.getPastTotalSupply` and `addresslistLengthAtBlock` instead.
- Removed `prepare*DataABI()` from `IPluginSetup` & `PluginSetup` and all the other contracts that inherit from `PluginSetup`.
- Removes `open` parameter from Multisig proposals.
- Removes `Tally` struct as well as `addressListLength` and moves `approvals` in `Proposal`.
- Removes `freeze` functionality.
- removes EIP-165 implementation from `ProposalBase`.

## v0.4.0-alpha

### Added

- Added the `Multisig` plugin and setup contract.
- Added a `VotingMode` enumeration to specify if the vote should be conducted in `Standard`, `EarlyExecution`, or `VoteReplacement` mode.
- Added the `Admin` plugin and setup contract.
- Added NFT compatibility by using OpenZeppelin's `IVotesUpgradeable` interface in `ERC20Voting` and renaming the contract to `TokenVoting`.
- Added extra check in `PermissionManager` to disallow giving DAO specific permissions to ANY_ADDR + giving any other permissions
  to ANY_ADDR unless oracle is passed. Also, freeze can only be used when where is not ANY_ADDR.
- Added `resolver` check in initialize function and `setDefaultResolver` of `ENSSubdomainRegistrar.sol`.
- Added test related to `resolver` in `ens-subdomain-registry.ts`.
- Added `_checkUpdateValidity` method to `PluginSetupProcessor` to prevent updates to the same or earlier versions that would lead to double initialization.
- Added more tests for the `PluginSetupProcessor`.
- Added `PluginSettings` to the `Multisig` plugin
- Added `onlyListed` to the `PluginSettings` of the `Multisig` plugin.

### Changed

- Abstracted the `Addresslist` to be used by `AddresslistVoting` and `Multisig`.
- Changed the order of the `_voteOption` and `_tryEarlyExecution` in `MajorityVoting`.
- The plugin-wide settings are now stored in a `private` `VotingSettings` struct and made available through getters.
- Structured the `getProposal` return data by adding a `struct ProposalParameters` and `struct Tally`.
- Bounded `minDuration` between one hour and one year and prevent integer overflows during the start date calculation (HAL-03, HAL-04).
- Changed `MajorityVoting` to use `minParticipation` and unified the parameter order.
- Fixed the early execution criterion in `MajorityVoting` by calculating the `worstCaseSupport` quantity.
- Renamed the names of folders, files, contracts, events, functions, and parameters in `MajorityVoting` to match with the SDK and Subgraph naming:
  - `AllowlistVoting` to `AddresslistVoting` and `allowlist` to `addresslist`
  - `VoteCreated` and `VoteExecuted` to `ProposalCreated` and `ProposalExecuted`
  - `voteId` to `proposalId`
  - `user` to `member`
- Fixed inheritance incompatibility with OZ contracts for `Plugin`, `PluginCloneable`, and `PluginUUPSUpgradeable`.
- Throw an error in `MajorityVoting` if the vote creator tries to vote before the start date.
- Refactored mocks for `PluginUUPSUpgradeable` and `PluginCloneable` and the respective setups.
- Moved `event.ts` from `/test/test-utils/` to `/utils/`.

### Removed

- Remove empty helpers array initialization in `AddresslistVotingSetup`.
- Removed the redundant base class `DaoAuthorizableBaseUpgradeable`.
- Removed `isApprovedForAll` check from initialize function of `ENSSubdomainRegistrar.sol`.
- Removed test related to `isApprovedForAll` in `ens-subdomain-registry.ts`.

## v0.3.0-alpha

### Added

- Added `00_create-plugins-repo.ts` for creating and registering plugin repo for plugins.
- Added `00_allowlist_voting_setup.ts` and `10_erc20_voting_setup.ts` for deploying plugin setup.
- Added `getMergedAbi()` function to `abi.ts`.
- Transferred the core docs from aragon/builders-portal to this repository.
- Added `AllowlistVotingSetup` and `ERC20VotingSetup`.
- Added utility functions (`deployPluginRepoRegistry`, `deployPluginSetupProcessor`, `deployPluginRepoFactory`, and `filterEvents`) to the test suite.
- Added `DaoAuthorizableBase` class.
- Added `DaoAuthorizableClonable` using OpenZeppelin initialization.
- Added mocks and tests for the `Plugin` and `PluginSetup` classes.
- Added `PluginSetupProcessor` to be the main class processing `PluginSetup` contracts and applying permissions in the installing DAO.
- Added `DaoAuthorizableUpgradeable` and a free `_auth` function to provide an `auth` modifier to the different plugin types and prevent code duplication.
- Added `PluginCloneable`, `PluginTransparentUpgradeable`.
- Added goerli configuration to deploy to the Goerli testnet.
- Added `AragonPlugin` and `AragonUpgradeablePlugin` for developers to inherit from for their concrete plugin implementations.
- Added helper function `test/test-utils/ens.ts` deploying the `ENSSubdomainRegistrar` and `ENS`-related contracts.
- Added Multi Target Bulk Permission object for `PermissionManager` with the oracle option as well.
- Added Abstract `PluginSetup` for the devs to inherit from for their concrete plugin manager implementation.
- Added the `solidity-docgen` hardhat plugin by OpenZeppelin to automatically generate documentation via `yarn docgen`.
- Added deployment script for `ENSSubdomainRegistrar`.
- Added `ENSSubdomainRegistrar` `Component` to register subdomains at the ENS.
- Added `IPluginRepo` interface for plugin PluginRepo contract.
- Added `PluginRepo` contract.
- Added `InterfaceBasedRegistry` base to be used for creating any ERC165-based registry such as DAO-Registry and `AragonPluginRegistry`.
- Added `AragonPluginRegistry` contract for registering `PluginRepo`s.
- Added `PluginRepoFactory` contract for creating `PluginRepo`s.
- Added testing for `PluginRepo`, `InterfaceBasedRegistry`, `AragonPluginRegistry` and `PluginRepoFactory`.
- Added deployment script for `managing-dao`, `plugin-registry` and `pluginRepo-factory`.
- Added an abstract `ERC165RegistryBase` `Component` to register contracts by their address based on their ERC165 interface ID.
- Added a concrete `ERC165Registry` implementation.
- Added ENS support for `PluginRepoRegistry`.
- Added minting functionality to the `initialize` function of `GovernanceERC20`.

### Changed

- Updated `Verify.ts` for verifying new contracts.
- Split `permissions.ts` into three files corresponding to `00_ens-permissions.ts`, `10_dao-registry-permissions.ts` and `20_plugin-registrty-permissions.ts`.
- Refactored `setupENS` function.
- Renamed `UPGRADE_PERMISSION` to be more specific to `UPGRADE_DAO_PERMISSION`, `UPGRADE_PLUGIN_PERMISSION`, etc.
- Refactored `DAOFactory`to use`PluginSetupProcessor`.
- Refactored NatSpec comments and names for the contracts related to the `Plugin` and `PluginSetup`.
- Renamed `PluginTransparentUpgradeable` to `PluginUpgradeable`.
- Refactored `AdaptiveERC165` into an independent `CallbackHandler` contract and separated `ERC165` from it.
- Adapted `Component` to use `DaoAuthorizableUpgradeable` until it is fully refactored to become `Plugin`.
- Refactored `DaoAuthorizable` to use the newly introduced, free `_auth` function to prevent code duplication.
- Improved `Counter` examples and added respective `PluginSetup` example contracts.
- Renamed `PluginManager` to `PluginSetup` and refactored it to be a two-transaction process consisting of a `prepare` and an `apply` step.
- Replaced `AragonPlugin` and `AragonUpgradeablePlugin` by `Plugin` and `PluginUUPSUpgradeable`, respectively.
- Changed `DAORegistry` to use the `ENSSubdomainRegistrar` so that a DAO name can only be registered once.
- Updated deploy script to correctly use `ERC1967Proxy`.
- Renamed `hasPermission` to `isGranted` in both `PermissionManager` and `IPermissionOracle`.
- Renamed several contracts, methods, variables, and constants as well as associated folder names.
- Updated deployment scripts for `managing-dao`, `dao-registry`, `aragon-plugin-registry`, `dao-factory`.
- Changed `registry.ts` to `dao-registry.ts` and updated testing.
- Changed `Registry` to `DAORegistry` and updated to inherit from `InterfaceBasedRegistry`.
- Bumped `@openzeppelin/contracts` and `@openzeppelin/contracts-upgradeable` to `4.7.0` and fixed `GovernanceWrappedERC20` accordingly.
- Refactored import statements.
- Changed `ERC165RegistryBase` to `InterfaceBasedRegistry`.
- Changed order of deployment scripts.
- Changed folder structure of tests.
- Refactored event names and NatSpec comments.
- Renamed `TestComponent`, `TestSharedComponent` to `TestPlugin`, `TestPluginComponent`.
- Renamed `createProxy` function to `createERC1967Proxy`.
- Replaces custom ERC1271 interface with Openzeppelins interface.
- Switched order of where and who for the events in `PermissionManager`.
- Extends `VersionCreated` event with `PluginSetup` and `contentURI`
- Markes parameters of `InstallationApplied` as `indexed`

### Removed

- Removed `AppStorage` and related helpers `PluginERC1967Proxy`, `TransparentProxy`.
- Removed `PluginConstants` that were related to the previous, indexd plugin setup solution.
- Removed restrictions regarding plugin's address in `PluginRepo`.
- Removed `deepEqual` overwrite of `equal` property in Chai Assertion used for testing of emitted events.
- Removed `ERC165Registry`.
- Removed `Component` and `MetaTxComponent`.
- Removed `MerkleMinter` deployment from `ERC20VotingSetup`.

## v0.2.0-alpha

### Added

- Added tests for the `ACL` and `IACLOracle`.
- Allow tokens to be minted to DAO's treasury by passing address(0) as receiver in `TokenFactory`.

### Changed

- Generalized `MerkleMinter` and made it a `MetaTxComponent`.
- Generalized `MerkleDistributor` and made it a `MetaTxComponent`.

### Removed

## v0.1.0-alpha

### Added

- Added workflow and scripts in `.github/helpers/contracts/dummy-dao/` to create dummy daos, deposits and proposals on contract deploy.
- Added `VoteConfig` struct in the `DAOFactory` to allow better typechain support for the creation of daos.
- Added `MetaTxComponent`.

### Changed

- Renamed the event `SetMetadata` to `MetadataSet`.
- Completed the `IDAO` interface and changed `DAO` accordingly.
- Decoupled `Permissions` from `BaseRelayRecipient`.
- Fixed OZ contracts-upgradeable `Initializable`.

### Removed

- Removed `Relay` interface from `Permissions.sol`.

## v0.0.1-alpha

### Added

- First version of the package, exposing the JSON artifacts.
