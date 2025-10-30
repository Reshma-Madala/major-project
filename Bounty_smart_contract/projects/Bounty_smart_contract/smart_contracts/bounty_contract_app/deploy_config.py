import logging
import algokit_utils

logger = logging.getLogger(__name__)

def deploy() -> None:
    # Import the generated client and args class from artifacts
    from smart_contracts.artifacts.bounty_contract_app.task_bounty_contract_client import (
        TaskBountyContractFactory,
        # If your contract has input args, import them here (e.g., InitArgs, etc.)
    )

    # Get an Algorand client from environment (works with localnet/testnet/mainnet)
    algorand = algokit_utils.AlgorandClient.from_environment()

    # Load deployer account from environment variable DEPLOYER
    deployer_ = algorand.account.from_environment("DEPLOYER")

    # Create a factory for your app
    factory = algorand.client.get_typed_app_factory(
        TaskBountyContractFactory, default_sender=deployer_.address
    )

    # Deploy the app (Create / Update / Replace)
    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    # Fund the app with 1 Algo if newly created
    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )

    logger.info(
        f"Deployed {app_client.app_name} (App ID: {app_client.app_id}) successfully!"
    )
