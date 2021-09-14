package helia.extensions

import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingCoalescingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.member
import com.kotlindiscord.kord.extensions.commands.converters.impl.user
import com.kotlindiscord.kord.extensions.commands.parser.Arguments
import com.kotlindiscord.kord.extensions.commands.slash.AutoAckType
import com.kotlindiscord.kord.extensions.extensions.Extension
import com.kotlindiscord.kord.extensions.utils.respond
import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.ButtonStyle
import dev.kord.core.behavior.edit
import dev.kord.core.behavior.ban
import dev.kord.core.behavior.interaction.edit
import dev.kord.core.entity.Message
import dev.kord.core.entity.interaction.PublicFollowupMessage
import dev.kord.rest.builder.message.create.embed
import dev.kord.rest.builder.message.modify.embed


import helia.TEST_SERVER_ID

import org.codehaus.groovy.ast.expr.Expression
import javax.script.ScriptEngineManager

@OptIn(KordPreview::class)
class CalculatorCommandH : Extension()   {
    override val name = "calculator"
    override suspend fun setup() {
        command() {
            name = "calculator"
            description = "Calculator command"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@CalculatorCommandH.kord
                val e = ScriptEngineManager().getEngineByName("js")
                var expression = ""
                lateinit var createmessage : Message


                createmessage = message.respond {
                    embed {
                        title = "Calculator"
                        description = "```PREP TEXT```"
                        components() {

                            interactiveButton {
                                label = "1"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "1"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }

                                }
                            }
                            interactiveButton {
                                label = "2"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "2"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "3"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "3"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "*"
                                style = ButtonStyle.Danger
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "*"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "EXIT"
                                style = ButtonStyle.Success
                                deferredAck = true

                                action { // Easy button actions
                                    createmessage.edit{
                                        this.embed {
                                            title = "Exiting embed"
                                            description = "```Closing calculator```"
                                        }
                                        components = mutableListOf()

                                    }
                                }
                            }
                            interactiveButton {
                                label = "4"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "4"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "5"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "5"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "6"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "6"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "÷"
                                style = ButtonStyle.Danger
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "/"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "←"
                                style = ButtonStyle.Success
                                deferredAck = true

                                action { // Easy button actions
                                    var n = 1
                                    var droponenum = expression.dropLast(n)
                                    expression = droponenum
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "7"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "7"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "8"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "8"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "9"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "9"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "+"
                                style = ButtonStyle.Danger
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "+"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "Clear"
                                style = ButtonStyle.Success


                                action { // Easy button actions
                                    expression = ""
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                    respond("Cleared the expression")
                                }
                            }
                            interactiveButton {
                                label = "00"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "00"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "0"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "0"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "."
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "."
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "-"
                                style = ButtonStyle.Danger
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "-"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "="
                                style = ButtonStyle.Success
                                deferredAck = true

                                action { // Easy button actions
                                    var result = e.eval(expression)
                                    var formatedres = result.toString()
                                    expression = formatedres
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${formatedres}```"

                                        }
                                    }



                                }
                            }
                            interactiveButton {
                                label = "("
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += "("
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = ")"
                                style = ButtonStyle.Secondary
                                deferredAck = true

                                action { // Easy button actions
                                    expression += ")"
                                    createmessage.edit{
                                        this.embed {
                                            title = "Calculator"
                                            description = "```${expression}```"

                                        }
                                    }
                                }
                            }
                            interactiveButton {
                                label = "π"
                                style = ButtonStyle.Secondary

                                action { // Easy button actions
                                    respond("Button  pressed!")
                                }
                            }
                        }


                    }
                }

            }
        }

        slashCommand() {
            name = "calculator"
            description = "Calculator command"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC


            //invite(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@CalculatorCommandH.kord
                val e = ScriptEngineManager().getEngineByName("js")
                var expression = ""
                lateinit var myResponse: PublicFollowupMessage





                myResponse = publicFollowUp {
                    embed {
                        title = "Calculator"
                        description = "```PREP TEXT```"

                    }
                    components() {

                        interactiveButton {
                            label = "1"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "1"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }

                            }
                        }
                        interactiveButton {
                            label = "2"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "2"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "3"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "3"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "*"
                            style = ButtonStyle.Danger
                            deferredAck = true

                            action { // Easy button actions
                                expression += "*"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "EXIT"
                            style = ButtonStyle.Success
                            deferredAck = true

                            action { // Easy button actions
                                myResponse.edit{
                                    this.embed {
                                        title = "Exiting embed"
                                        description = "```Closing calculator```"
                                    }
                                    components = mutableListOf()

                                }
                            }
                        }
                        interactiveButton {
                            label = "4"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "4"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "5"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "5"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "6"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "6"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "÷"
                            style = ButtonStyle.Danger
                            deferredAck = true

                            action { // Easy button actions
                                expression += "/"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "←"
                            style = ButtonStyle.Success
                            deferredAck = true

                            action { // Easy button actions
                                var n = 1
                                var droponenum = expression.dropLast(n)
                                expression = droponenum
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "7"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "7"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "8"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "8"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "9"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "9"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "+"
                            style = ButtonStyle.Danger
                            deferredAck = true

                            action { // Easy button actions
                                expression += "+"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "Clear"
                            style = ButtonStyle.Success


                            action { // Easy button actions
                                expression = ""
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                                respond("Cleared the expression")
                            }
                        }
                        interactiveButton {
                            label = "00"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "00"
                                respond("```${expression}```")
                            }
                        }
                        interactiveButton {
                            label = "0"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "0"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "."
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "."
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "-"
                            style = ButtonStyle.Danger
                            deferredAck = true

                            action { // Easy button actions
                                expression += "-"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "="
                            style = ButtonStyle.Success
                            deferredAck = true

                            action { // Easy button actions
                                var result = e.eval(expression)
                                var formatedres = result.toString()
                                expression = formatedres
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${formatedres}```"

                                    }
                                }



                            }
                        }
                        interactiveButton {
                            label = "("
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "("
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = ")"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += ")"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                        interactiveButton {
                            label = "π"
                            style = ButtonStyle.Secondary
                            deferredAck = true

                            action { // Easy button actions
                                expression += "3,1415926535"
                                myResponse.edit{
                                    this.embed {
                                        title = "Calculator"
                                        description = "```${expression}```"

                                    }
                                }
                            }
                        }
                    }
                }

            }
        }
    }
}