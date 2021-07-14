/*
 * MIT License
 *
 * Copyright (c) 2020 Airbyte
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package io.airbyte.integrations.destination.rockset;

import com.fasterxml.jackson.databind.JsonNode;
import com.google.common.collect.ImmutableMap;
import com.rockset.client.model.CreateWorkspaceRequest;
import com.rockset.client.model.CreateWorkspaceResponse;
import com.rockset.client.ApiException;
import com.rockset.client.RocksetClient;
import com.rockset.jdbc.RocksetDriver;
import io.airbyte.commons.json.Jsons;
import io.airbyte.integrations.BaseConnector;
import io.airbyte.integrations.destination.jdbc.AbstractJdbcDestination;
import io.airbyte.integrations.base.AirbyteMessageConsumer;
import io.airbyte.integrations.base.Destination;
import io.airbyte.integrations.base.IntegrationRunner;
import io.airbyte.integrations.destination.jdbc.DefaultSqlOperations;
import io.airbyte.protocol.models.AirbyteConnectionStatus;
import io.airbyte.protocol.models.AirbyteConnectionStatus.Status;
import io.airbyte.protocol.models.AirbyteMessage;
import io.airbyte.protocol.models.ConfiguredAirbyteCatalog;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.Consumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class RocksetDestination extends BaseConnector implements Destination {

  private static final Logger LOGGER = LoggerFactory.getLogger(RocksetDestination.class);

  private static final String WORKSPACE_ID = "workspace";
  private static final String API_KEY_ID = "api_key";

  private static final String APISERVER_URL = "api.rs2.usw2.rockset.com";

  public static void main(String[] args) throws Exception {
    new IntegrationRunner(new RocksetDestination()).run(args);
  }

  @Override
  public AirbyteConnectionStatus check(JsonNode config) {
    try {
      String workspace = config.get(WORKSPACE_ID).asText();
      String apiKey = config.get(API_KEY_ID).asText();
      createWorkspaceIfNotExists(apiKey, workspace);
      return new AirbyteConnectionStatus().withStatus(Status.SUCCEEDED);
    } catch (Exception e) {
      LOGGER.info("Check failed.", e);
      return new AirbyteConnectionStatus().withStatus(Status.FAILED).withMessage(e.getMessage() != null ? e.getMessage() : e.toString());
    }
  }

  private void createWorkspaceIfNotExists(String apiKey, String workspace) throws Exception {
    RocksetClient client = new RocksetClient(apiKey, APISERVER_URL);
    CreateWorkspaceRequest request = new CreateWorkspaceRequest()
      .name(workspace);

    try {
      CreateWorkspaceResponse response = client.createWorkspace(request);
      LOGGER.info(String.format("Created workspace %s", workspace));
    } catch (ApiException e) {
      if (e.getCode() == 400) {
        LOGGER.info(String.format("Workspace %s already exists", workspace));
        return;
      }

      throw e;
    }
  }

  @Override
  public AirbyteMessageConsumer getConsumer(
      JsonNode config,
      ConfiguredAirbyteCatalog catalog,
      Consumer<AirbyteMessage> outputRecordCollector) throws Exception {
    // TODO
    return null;
  }
}