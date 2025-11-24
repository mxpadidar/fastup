import asyncio

from fastup.core.services import IDGenerator


async def test_ids_generated_in_a_batch_are_all_unique(idgen: IDGenerator):
    """
    Ensures that when a single generator instance creates many IDs in quick
    succession, every ID is unique.
    """
    # Generate 1,000 IDs to test the sequence part of the generator
    ids = [await idgen.next_id() for _ in range(1_000)]

    # Verifies uniqueness by comparing the list length to the set length
    assert len(ids) == len(set(ids))


async def test_a_later_id_is_always_greater_than_an_earlier_id(idgen: IDGenerator):
    """
    Verifies the time-sortable property by confirming that an ID generated
    at a later time is numerically greater than one generated earlier.
    """

    first_id = await idgen.next_id()
    await asyncio.sleep(0.001)  # Ensure the millisecond timestamp can advance
    second_id = await idgen.next_id()

    assert second_id > first_id


async def test_a_sequence_of_generated_ids_is_correctly_sorted(idgen: IDGenerator):
    """
    Checks the monotonic nature of the generator by ensuring a list of
    generated IDs is already in ascending order.
    """
    ids = [await idgen.next_id() for _ in range(1_000)]

    # A list of monotonically increasing numbers should already be sorted
    assert ids == sorted(ids)
