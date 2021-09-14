package helia.extensions


import com.kotlindiscord.kord.extensions.commands.converters.impl.*
import com.kotlindiscord.kord.extensions.commands.parser.Arguments
import com.kotlindiscord.kord.extensions.commands.slash.AutoAckType
import com.kotlindiscord.kord.extensions.extensions.Extension
import com.kotlindiscord.kord.extensions.utils.respond
import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.ButtonStyle
import dev.kord.common.entity.Snowflake
import dev.kord.core.behavior.edit
import dev.kord.core.behavior.interaction.edit
import dev.kord.core.cache.data.MessageData
import dev.kord.core.entity.Message
import dev.kord.core.entity.channel.GuildMessageChannel
import dev.kord.core.entity.interaction.PublicFollowupMessage
import dev.kord.rest.builder.message.create.embed
import dev.kord.rest.builder.message.modify.embed
import kotlinx.coroutines.InternalCoroutinesApi
import kotlinx.coroutines.flow.FlowCollector

@InternalCoroutinesApi
@OptIn(KordPreview::class)
class PurgeCommandH : Extension()   {
    // placeholder for purge command
    override val name = "purge"
    override suspend fun setup() {
        command(::purgeArgs) {
            name = "purge"
            description = "Clear an ammount of messages"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@PurgeCommandH.kord

                var args = arguments
                lateinit var createmessage : Message



                createmessage = message.respond {
                    var getterchannel = message.channel
                    embed {
                        title = "Purge command"
                        description = "Do you want to purge {placeholder} messages?"
                        components() {
                            interactiveButton {
                                label = "✓"
                                style = ButtonStyle.Success
                                deferredAck = true

                                action { // Easy button actions
                                    var initchanbulk = getterchannel as? GuildMessageChannel ?


                                    //var flowcollx :  FlowCollector<Message>
                                    //flowcollx = getterchannel.getMessagesBefore(myResponse.id,args.numbercount)

                                    //var exmes: Message

                                    //var transitionper:Snowflake

                                    //var ids: Iterable<Snowflake> = mutableListOf();

                                    //while (ids.count() <args.numbercount) {

                                    //transitionper = exmes.id
                                    //ids += transitionper
                                    //}
                                    //initchanbulk?.bulkDelete(ids)
                                    createmessage.edit{
                                        this.embed {
                                            title = "Action Complete"
                                            description = "```Purged Messages```"
                                        }
                                        components = mutableListOf()

                                    }


                                }
                            }
                            interactiveButton {
                                label = "X"
                                style = ButtonStyle.Danger
                                deferredAck = true

                                action { // Easy button actions
                                    createmessage.edit{
                                        this.embed {
                                            title = "Action Aborted"
                                            description = "```The action was aborted due to refusal action```"

                                        }
                                    }
                                }
                            }
                        }

                    }
                }

            }
        }

        slashCommand(::purgeSlashArgs) {
            name = "purge"
            description = "Clear an ammount of messages"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //guild(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@PurgeCommandH.kord

                var args = arguments
                lateinit var myResponse: PublicFollowupMessage


                myResponse = publicFollowUp {
                    var getterchannel = myResponse.channel
                    embed {
                        title = "Purge command"
                        description = "Do you want to purge {placeholder} messages?"
                    }
                    components() {
                        interactiveButton {
                            label = "✓"
                            style = ButtonStyle.Success
                            deferredAck = true

                            action { // Easy button actions
                                var initchanbulk = getterchannel as? GuildMessageChannel ?

                                //var flowcollx :  FlowCollector<Message>
                                //flowcollx = getterchannel.getMessagesBefore(myResponse.id,args.numbercount)

                                //var exmes: Message

                                //var transitionper:Snowflake

                                //var ids: Iterable<Snowflake> = mutableListOf();

                                //while (ids.count() <args.numbercount) {

                                    //transitionper = exmes.id
                                    //ids += transitionper
                                //}
                                //initchanbulk?.bulkDelete(ids)
                                myResponse.edit{
                                    this.embed {
                                        title = "Action Complete"
                                        description = "```Purged Messages```"
                                    }
                                    components = mutableListOf()
                                }

                            }
                        }
                        interactiveButton {
                            label = "X"
                            style = ButtonStyle.Danger
                            deferredAck = true

                            action { // Easy button actions
                                myResponse.edit{
                                    this.embed {
                                        title = "Action Aborted"
                                        description = "```The action was aborted due to refusal action```"
                                    }
                                    components = mutableListOf()
                                }
                            }
                        }
                    }
                }

            }
        }

    }


    inner class purgeArgs : Arguments() {
        val numbercount by int(displayName = "count",description = "weird")

        val reason by defaultingCoalescingString(
            "reason",

            defaultValue = "Nothing",
            description = "What's the reason you want to purge the chat"
        )
    }

    inner class purgeSlashArgs : Arguments() {
        val numbercount by int(displayName = "count",description = "weird")

        // Coalesced strings are not currently supported by slash commands
        val reason by defaultingString(
            "reason",

            defaultValue = "Nothing",
            description = "What's the reason you want to purge the chat"
        )
    }
}