#
# MIT License
#
# Copyright (c) 2020 Airbyte
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from json import loads

import responses
from airbyte_cdk.models import SyncMode
from jsonschema import validate
from source_amazon_ads import SourceAmazonAds


@responses.activate
def test_streams_profile(test_config, profiles_response):
    source = SourceAmazonAds()
    streams = source.streams(test_config)
    assert len(streams) == 1
    profile_stream = streams[0]
    assert profile_stream.name == "profiles"
    schema = profile_stream.get_json_schema()
    responses.add(
        responses.POST,
        "https://api.amazon.com/auth/o2/token",
        json={"access_token": "alala", "expires_in": 10},
    )
    responses.add(
        responses.GET,
        "https://advertising-api.amazon.com/v2/profiles",
        body=profiles_response,
    )

    records = profile_stream.read_records(SyncMode.full_refresh)
    records = [r for r in records]
    assert len(responses.calls) == 2
    assert len(records) == 4
    expected_records = loads(profiles_response)
    for record, expected_record in zip(records, expected_records):
        validate(schema, record)
        assert record == expected_record
